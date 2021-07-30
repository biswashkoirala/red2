from fastapi import FastAPI , Depends, status
from fastapi.exceptions import HTTPException
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
    new_blog = models.Blog(title=request.title, body=request.body,user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200, response_model=schemas.ShowBlog,tags=['blogs'])
def show(id, response: Response, db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with id {id} is not available')
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

@app.put('/blog/{id}/upvote',status_code=status.HTTP_202_ACCEPTED)
def upvote(id, db:Session=Depends(get_db)):
    score = db.query(models.Blog).filter(models.Blog.id==id).first().score
    db.query(models.Blog).filter(models.Blog.id==id).update({'score':score+1})
    db.commit()
    return f'Score for BLog with id {id} upvoted'

@app.put('/blog/{id}/downvote',status_code=status.HTTP_202_ACCEPTED)
def downvote(id, db:Session=Depends(get_db)):
    score = db.query(models.Blog).filter(models.Blog.id==id).first().score
    db.query(models.Blog).filter(models.Blog.id==id).update({'score':score-1})
    db.commit()
    return f'Score for BLog with id {id} downvoted'


@app.get('/')
def index():
    return 'This is the homepage'


@app.post('/user',response_model=schemas.ShowUser)
def create_user(request: schemas.User, db:Session=Depends(get_db)):
    new_user=models.User(name=request.name, email=request.email,password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user')
def all(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get('/user/{id}',response_model=schemas.ShowUser)
def get_user(id:int, db:Session=Depends(get_db)):
    user =db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user with id {id} not available')
    return user