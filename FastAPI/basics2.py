from fastapi import FastAPI,Path,Query,Body
from enum import Enum
from pydantic import BaseModel

class UserType(str, Enum):
    # accept
    STANDARD = "standard"
    ADMIN = "admin"


app = FastAPI()

@app.get("/users/{id}")
async def get_user(id:int):
    return {'id':id}



@app.get("/users/{type}/{id}")
async def get_users(type: UserType, id: int):
    return {"type": type, "id": id}


@app.get("/users/{id}")
async def get_userss(id:int=Path(...,ge=1)):
    # ... ellipsis syntax as the first parameter of Path (we don't want default params)
    # int should greater than one
    return {"id":id}


@app.get("/license-plates/{license}")
async def get_license_plate(license:str = Path(...,min_length=9,max_length=9,regex=r"^\w{2}-\d{3}-\w{2}$")):
    return {"license":license}



@app.get("/admins")
async def get_admins(page:int=Query(1,gt=0),size:int=Query(10,le=100)):
    return {'page':page,'size':size}



class User(BaseModel):
    name: str
    age: int


@app.get("/users")
async def create_user(user:User, priority:int=Body(...,ge=1,le=3)):
    return {"user":user,"priority":priority}
