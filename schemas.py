from typing import List
from pydantic import BaseModel



class BlogBase(BaseModel):
    title: str
    body: str
    #score: int
    

class Blog(BlogBase):
    class Config():
        orm_mode = True




class User(BaseModel):
    name: str
    email:str
    password:str



class ShowUser(BaseModel):
    name: str
    email:str
    blogs: List[Blog]=[]
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title:str
    body:str
    creator: ShowUser

    class Config():
        orm_mode=True




# schemas : for view type. edit the view : pydantic
# models : for main database structure : SQLite