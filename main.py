from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

todoapp = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@todoapp.get("/")
def index():
    return {"FastAPI SQL Database": "Maria Clarin (2501990331) L4AC"}

@todoapp.post("/create-new-user/", response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@todoapp.post("/create-user-todolist/{user_id}", response_model=schemas.Todo)
def create_user_todolist(
    user_id: int, todo: schemas.CreateTodo, db: Session = Depends(get_db)):
    return crud.create_user_todo(db=db, todo=todo, user_id=user_id)

@todoapp.get("/get-users/", response_model=list[schemas.User])
def get_user(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_user_list(db, skip=skip, limit=limit)
    return users

@todoapp.get("/get-user-by-id/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@todoapp.get("/get-todolist/", response_model=list[schemas.Todo])
def get_todo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todolist(db, skip=skip, limit=limit)
    return todos

@todoapp.delete("/delete-user/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db, user_id=user_id)