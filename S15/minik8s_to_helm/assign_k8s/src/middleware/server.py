import io
import os
import zlib
import json
import socket
import logging
from contextlib import asynccontextmanager
import requests
import traceback


import redis.asyncio as redis
import httpx

from PIL import Image
from fastapi import FastAPI, File, Depends,HTTPException,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from typing import Dict, Annotated,Union


# Update environment variables
MODEL_SERVER_URL = os.environ.get("MODEL_SERVER_URL","http://localhost:8081") # http://modelserver-service:8000
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")                        # http://redis-service
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
HOSTNAME = socket.gethostname()


# Configure logging
logging.basicConfig(filename='middleware.log', level=logging.INFO, format="%(asctime)s - FastAPI - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_pool
    logger.info(f"Initializing Redis server on host {HOSTNAME}")

    # Redis setup
    logger.info(f"Creating Redis connection pool: host={REDIS_HOST}, port={REDIS_PORT}")
    redis_pool = redis.ConnectionPool(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        db=0,
        decode_responses=True,
    )

    try:
        logger.info("Redis initialization complete")
        yield
    finally:
        logger.info("Shutting down Redis server")
        # await redis_pool.disconnect()  # Disconnect the connection pool
        await redis_pool.aclose()      # Disconnect all the connection pool
        logger.info("Cleanup complete")

app = FastAPI(title="Middleware Server",lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_redis():
    return redis.Redis(connection_pool=redis_pool)


async def write_to_cache(file: bytes, result: Dict[str, float]) -> None:
    cache = get_redis()
    hash = str(zlib.adler32(file))
    print('*'*100)
    print(type(file),type(result),result)
    print('*'*100)
    logger.debug(f"Writing prediction to cache with hash: {hash}")
    await cache.set(hash, json.dumps(result))
    logger.debug("Cache write complete")

async def check_cached(image: bytes):
    hash = zlib.adler32(image)
    cache = get_redis()

    logger.debug(f"Checking cache for image hash: {hash}")
    data = await cache.get(hash)

    if data:
        logger.info(f"Cache hit for image hash: {hash}")
    else:
        logger.info(f"Cache miss for image hash: {hash}")

    return json.loads(data) if data else None



@app.get("/")
def read_root():
    return {"Hello": "Planet! 🌎"}

@app.get("/health")
async def health_check():
    try:
        redis_client = get_redis()
        redis_connected = await redis_client.ping()
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}")
        redis_connected = False

    try:
        # healthcheck
        model_connected = False
        model_res = requests.get(f"{MODEL_SERVER_URL}/health")
        if model_res.status_code==200:
            r:Dict = model_res.json()
            model_connected = True
            logger.info(f"Model Running Condition: {str(r.get('status'))}")
        else:
            logger.warning("Model Running Condition: Abnormal")
        
    except Exception as e:
        logger.error(f"Model health check failed: {str(e)}")

    return {
        "status": "healthy",
        "hostname": HOSTNAME,
        "model":{
            "connected":model_connected,
        },
        "redis": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "connected": redis_connected,
        },
    }


async def infer(image:Annotated[bytes, File()]):
    '''
        helper utilities for inference
        - make predicition on model_prediction_url
        - write to cache

        modelserver will handle io.Byte for requests
    '''
    logger.info("Received inference request")
    logger.debug("Running prediction")
    # input::   Image
    # output::  Dict[str:float]
    files = {"image": image}
    predictions = requests.post(url=f'{MODEL_SERVER_URL}/fdogs',files=files)
    print('*'*100)
    print(predictions.json(),type(predictions.json()))
    print('*'*100)
    logger.info(f"Prediction for inference request {predictions} ")
    logger.debug("Writing results to cache")
    await write_to_cache(image, predictions.json())

    logger.info("Inference complete")
    return predictions.json()



@app.post("/classify-catdog")
async def classify_catdog(image:Annotated[bytes, File()]): 
    logger.info("Received classification request")
    infer_cache = await check_cached(image) # else None
    if infer_cache == None:
        logger.info("Making request to model server")
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
            try:
                logger.info("sending files")
                logger.debug(f"Sending request to model server: {MODEL_SERVER_URL}")
                response = await infer(image=image)
                logger.info("got response")
                # response.raise_for_status()
                logger.info("Successfully received model prediction")
                return response
            except Exception as e:
                traceback.print_exc()
                logger.error(f"Model server request failed: {str(e)}")
                raise HTTPException(status_code=500, detail="Error from Model Endpoint")
    return infer_cache
