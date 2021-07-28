from fastapi import FastAPI , Depends
from fastapi.param_functions import Body
from sqlalchemy.orm import Session
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


@app.get('/')
def index():
    return 'This is the homepage'