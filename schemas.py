from pydantic import BaseModel

class TodoBase(BaseModel):
    name: str
    description: str
    completed: bool

class CreateTodo(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
    
class UserBase(BaseModel):
    username: str
    email: str
    auth: str

class CreateUser(UserBase):
    pass

class User(UserBase):
    id: int
    todolist: list[Todo] = []

    class Config:
        orm_mode = True