from fastapi import FastAPI,HTTPException,status,Depends
from typing import Any,Dict

blogs:Dict = {
    '1':'pre-requesits',
    '2':'websockets',
    '3':'building ml models'
}

users:Dict = {
    '1':'muthu',
    '2':'raj'
}

models:Dict = {
    '1':'linear',
    '2':'logistic',
    '3':'Neural Network'
}


app:FastAPI = FastAPI(title="Dependency Injection",description="study")


def get_blog_or_404(id:str):
    blog = blogs.get(id)
    if not blog:
        raise HTTPException(detail="Blog with id doesn't exists",status_code=status.HTTP_404_NOT_FOUND)
    return  blog

@app.get("/blog/{id}")
def get_blog(blog_name:str=Depends(get_blog_or_404)):
    return blog_name





# def get_object_or_404(dictionary:Dict,id:str):
#     obj = dictionary.get(id)
#     if not obj:
#         raise HTTPException(detail="Object with id doesn't exists",status_code=status.HTTP_404_NOT_FOUND)
#     return obj

# WE CAN"T PASS (user,id) in FASTAPI ☠️🚨💀
# @app.get("/object/{id}")
# def get_object(object=Depends(get_object_or_404(user,id))):
#     return object


class GetObjectOr404:
    ''' Parametrized Dependencies '''
    def __init__(self,dictionary:Dict) -> None:
        self.dictionary:Dict = dictionary

    def __call__(self,id:str) -> Any:
        '''every Depedency Injection needs callable function'''
        obj:str = self.dictionary.get(id)
        if not obj:
            raise HTTPException(detail="Object with id doesn't exists",status_code=status.HTTP_404_NOT_FOUND)
        return obj



user_dependecy = GetObjectOr404(dictionary=users)
@app.get("/user/{id}")
def get_users(user_name:str=Depends(dependency=user_dependecy)):
    return user_name



model_dependency = GetObjectOr404(dictionary=models)
@app.get("/model/{id}")
def get_user(model_name:str=Depends(dependency=model_dependency)):
    return model_name
