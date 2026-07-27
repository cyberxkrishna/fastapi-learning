from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI()



'''
@app.get("/")
def home():
    return "Krishna"

@app.get("/about")
def about():
    return {"Description":"This is about page "}

#Dynamic parameters

# Path parameters

@app.get("/users/{user_id}")
def user(user_id:int):
    return {"user_id":user_id}

# Query and optional params

@app.get("/user")
def name(name: str = "hello" ): # we can put any default value but generally null is used like this--- /def name(name: str = None ).
    return{"username":name} 

#default
@app.get("/product")
def user1(limit:int=10):
    return{"Limit":limit}

#multiple query params

@app.get("/products")
def product(name:str,price:int=100000000):
    return{
        "Name":name,
        "Price":price
    }


##### REQUEST BODY ### POST ######

@app.post("/new_user")
def create_new_user(name:str,Address:str,age:int,detail:dict):
    return{
        "name":name,
        "Address":Address,
        "age":age,
        "detail":detail
    }


## Data validation using pydantic.
class User(BaseModel):
    name:str
    age:int

@app.post("/create_new")
def new(user:User):
    return{
        "User is created":"lol",
        "User":user
    }


#nested data validation using pydantic

class new_user(BaseModel):
    name:str
    age:int

class address(BaseModel):
    city:str
    pincode:int
    user_detail:new_user

@app.post("/new")
def new1_user(new:address):
    return{"All detail":new}

    
'''

##### TODO API USING CRUD operation #####
'''
todos=[]

class Todo(BaseModel):
    id:int
    title:str
    completed:bool


@app.post("/todos")
def todo(todo:Todo):
    todos.append(todo)
    return{
        "massage":"Todo added","data":todo
    }

@app.get("/todos")
def get_todo():
    return todos

@app.get("/todos/{todo_id}")
def get_tods(todo_id:int):
    for todo in todos:
        if todo.id==todo_id:
            return todo
    return{"Not existed"}

@app.put("/todos/{todo_id}")
def update_todo(todo_id:int,update_todo:Todo):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            todos[index]=update_todo
            return{
                "message":"Data updated",
                "data":update_todo
            }
    return{"Not todo existed"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            todos.pop(index)
            return {
                "Todo deleted successfully"}
    return{"Not found"}

'''
##### RESPONSE MODEL #####

class user(BaseModel):
    name:str
    age:int
    password:int

class UserResponse(BaseModel):
    name:str
    age:int

@app.get("/user")
def user():
    return{
        "name":"Krishna",
        "age":21,
        "password":1235456
    }
