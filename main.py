from fastapi import FastAPI , Depends, status
from fastapi.param_functions import Body
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT
import schemas, models
from database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post('/blog')
def create(request: schemas.Blog, db:Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def show(id, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db:Session=Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db:Session=Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({'title':request.title, 'body':request.body})
    db.commit()
    return f'BLog with id {id} updated'


@app.get('/')
def index():
    return 'This is the homepage'


@app.post('/user')
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    new_user=models.User(name=request.name, email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
