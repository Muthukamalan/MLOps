import random

from fastapi import FastAPI,HTTPException,Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import prometheus_client



heads_count  =prometheus_client.Counter(
    name="heads_count",
    documentation="Number of heads"
)

tails_count  =prometheus_client.Counter(
    name="tails_count",
    documentation="Number of tails"
)
flip_count  =prometheus_client.Counter(
    name="flip_count",
    documentation="Number of flips"
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/flip-coins")
async def flip_coins(times=None):
    if times is None or not times.isdigit():
        raise HTTPException(status_code=400,detail="times must be set in request and an integer")
    times_as_int=int(times)
    heads = 0
    for _ in range(times_as_int):
        if random.randint(0,1):
            heads+=1 
    tails = times_as_int - heads

    heads_count.inc(heads)
    tails_count.inc(tails)
    flip_count.inc(times_as_int)

    return {
        "heads":heads,
        "tails":tails 
    }



@app.get("/metrics")
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )




if __name__=='__main__':
    uvicorn.run(app=app,host="0.0.0.0",port=5000)