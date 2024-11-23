import os 
import asyncio 
import contextlib 
import io 
from pathlib import Path

import torch
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel
from transformers import YolosForObjectDetection,YolosImageProcessor

os.environ["TRANSFORMERS_CACHE"] = "."

class Object(BaseModel):
    box:tuple[float,float,float,float]
    label:str 


class Objects(BaseModel):
    objects:list[Object]


class ObjectDetection:
    image_processor: YolosImageProcessor|None =None
    model          : YolosForObjectDetection|None = None


    def load_model(self)->None:
        "Loads the model"
        self.image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
        self.model           = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")
        print("Model loaded !!")

    def predict(self,image:Image.Image)->Objects:
        "Runs prediction"
        if not self.image_processor:
            raise RuntimeError("Processor is not loaded")
        if not self.model:
            raise RuntimeError("Model is not loaded")
        inputs = self.image_processor(images=image,return_tensors="pt")
        outputs= self.model(**inputs)
        target_size = torch.tensor([image.size[::-1]])
        results = self.image_processor.post_process_object_detection(outputs=outputs,threshold=.7,target_sizes=target_size)[0]

        objects:list[Object] = []
        for score, label, box in zip(
            results['scores'], results['labels'], results['boxes']
        ):
             if score>0.7:
                box_values = box.tolist()
                label      = self.model.config.id2label[label.item()]
                objects.append(Object(box=box_values,label=label))
        return Objects(objects=objects)
    

object_detection = ObjectDetection()

@contextlib.asynccontextmanager
async def lifespan(app:FastAPI):
    object_detection.load_model()
    yield

app = FastAPI(lifespan=lifespan)


async def receive(websocket:WebSocket,queue:asyncio.Queue):
    while True:
        bytes = await websocket.receive_bytes()
        try:
            queue.put_nowait(bytes)
            # Put an item into the queue without blocking. 
            # If no free slot is immediately available, raise QueueFull.
        except asyncio.QueueFull:
            pass 

async def detect(websocket:WebSocket, queue:asyncio.Queue):
    while True:
        bytes = await queue.get()
        image = Image.open(io.BytesIO(bytes))
        objects = object_detection.predict(image=image)
        await websocket.send_json(objects.dict())

@app.websocket("/object-detection")
async def ws_object_detection(websocket:WebSocket):
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=1)
    receive_task = asyncio.create_task( receive(websocket,queue=queue) )
    detect_task  = asyncio.create_task( detect(websocket=websocket,queue=queue))
    try:
        done,pending = await asyncio.wait( fs={receive_task,detect_task},return_when=asyncio.FIRST_COMPLETED )
        for task in pending:
            task.cancel()
        for task in done:
            task.result()
    except WebSocketDisconnect:
        pass 



@app.get("/")
async def index():
    '''serves homepage for our website'''
    return FileResponse(Path(__file__).parent / "index.html")


static_files_app = StaticFiles(directory=Path(__file__).parent / "assets")
app.mount("/assets", static_files_app)


# if __name__=="__main__":
#     import uvicorn
#     uvicorn.run(app)