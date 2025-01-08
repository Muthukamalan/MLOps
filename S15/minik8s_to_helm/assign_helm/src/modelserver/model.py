import psutil
from fastapi  import FastAPI,File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import io
from typing import Dict, Annotated,Union
import contextlib
import numpy as np 
import onnxruntime as ort 
import socket
import logging
import datetime 
host_name =  socket.gethostname()

# Configure logging
logging.basicConfig(
     filename='dogbreeds-modelserver.log',
     level=logging.INFO, 
     format= "%(asctime)s - ONNXModel - %(levelname)s - %(message)s",
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
logger.info(f"model server on host {host_name} and starts at {datetime.datetime.utcnow()}")

class_labels = [
    "Beagle",
    "Boxer",
    "Bulldog",
    "Dachshund",
    "German_Shepherd",
    "Golden_Retriever",
    "Labrador_Retriever",
    "Poodle",
    "Rottweiler",
    "Yorkshire_Terrier",
]


INPUT_SIZE = (224, 224)
MEAN = np.array([0.485, 0.456, 0.406])
STD = np.array([0.229, 0.224, 0.225])

def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")                            # Convert to RGB if not already
    image = image.resize(INPUT_SIZE)                        # Resize
    img_array = np.array(image).astype(np.float32) / 255.0  # Convert to numpy array and normalize
    img_array = (img_array - MEAN) / STD                    # Apply mean and std normalization
    img_array = img_array.transpose(2, 0, 1)                # Transpose to channel-first format (NCHW)
    img_array = np.expand_dims(img_array, 0)                # Add batch dimension
    return img_array



class Dogsprediction:
    def load_model(self)->None:
        logger.info(f"model loading on {datetime.datetime.utcnow()}")
        self.session = ort.InferenceSession('mambaout.onnx')
        self.session_input_name = self.session.get_inputs()[0].name
    
    def predict(self,image:Image.Image):
        logger.info(f"prediction starts on received image {datetime.datetime.utcnow()}")
        img = preprocess_image(image=image)
        outputs = self.session.run(None,{self.session_input_name:img.astype(np.float32)})
        logits = outputs[0][0]
        probabilities = np.exp(logits) / np.sum(np.exp(logits))
        # predictions = {class_labels[i]: float(prob) for i, prob in enumerate(probabilities)}
        predicted_label = class_labels[np.argmax(probabilities)]
        confidence = np.max(probabilities)
        logger.info(f"prediction ends on received image {datetime.datetime.utcnow()}")
        return {
            'confidence': str(float(confidence)),
            'label':str(predicted_label)
        }

    
dog_prediction = Dogsprediction()

@contextlib.asynccontextmanager
async def lifespan(app:FastAPI):
    dog_prediction.load_model()
    yield

app = FastAPI(title="Image Classification API",lifespan=lifespan,description="FastAPI application serving an ONNX model for image classification",    version="1.0.0",)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/fdogs",response_model=dict)
async def post_object_detection(image:Annotated[bytes, File(),bytearray])->dict:
    logger.info(f"Image received at {datetime.datetime.utcnow()} and its type {type(image)}")

    print('*'*100)
    print(type(image))
    print('*'*100)
    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image)).convert('RGB')  # Convert byte data to PIL Image
    elif isinstance(image, bytearray):
        image = Image.open(io.BytesIO(image)).convert('RGB')
    elif isinstance(image, str):    
        image = image.encode("utf-8")          # Decode string data:: byteArray
        image = Image.open(io.BytesIO(image))

    image_objext = image.convert("RGB")
    return dog_prediction.predict(image_objext)


@app.get("/health")
async def health_check():
    logger.info(f"Healthcheck hits at {datetime.datetime.utcnow()}")
    return JSONResponse(
        content={"status": "healthy", "model_loaded": True, 'hostname':host_name}, status_code=200
    )
 

@app.get("/metrics")
def get_metrics():
    logger.info(f"Metrics hits at {datetime.datetime.utcnow()}")
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    thread_count = psutil.Process().num_threads()

    metrics = {
        "cpu_usage_percent": cpu_usage,
        "memory": {
            "total_gb": memory.total / (1024 ** 3),
            "available_gb": memory.available / (1024 ** 3),
            "used_gb": memory.used / (1024 ** 3),
            "usage_percent": memory.percent
        },
        "disk": {
            "total_gb": disk.total / (1024 ** 3),
            "used_gb": disk.used / (1024 ** 3),
            "free_gb": disk.free / (1024 ** 3),
            "usage_percent": disk.percent
        },
        "thread_count": thread_count
    }

    return metrics

if __name__=='__main__':
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port='8000')

