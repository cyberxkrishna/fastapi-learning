from fastapi import FastAPI,status,HTTPException,Request,Depends,Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time
import sqlite3


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

'''

##### RESPONSE MODEL #####

class user(BaseModel):
    name:str
    age:int
    password:int

class UserResponse(BaseModel):
    name:str
    age:int

@app.get("/user",response_model=UserResponse)
def user():
    return{
        "name":"Krishna",
        "age":25,
        "password":2352
    }

'''


##### STATUS CODE AND RESPONSES #####

'''
#here we have to import http
@app.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user():
    return{
        "User created"
        }

# custom response
@app.get("/user")
def get_user():
    return{
        "Message":"User created",
        "Status":"Success",
        "User":{
            "Name":"Krishna",
            "age":25
        }
    }
'''


#### Exception handling ####

# Error handling (here we have to import http exception)
'''
@app.get("/user/{user_id}")
def users(user_id:int):
    if user_id!=12:
        raise HTTPException(
            status_code=404,
            detail="user not fouund"
        )
    else:
        return{
            "name":"Krishna",
            "age":25
        }
        '''
    
# custom error handling
'''

class UsersNotFound(Exception):
    def __init__(self,name):
        self.name=name

@app.get("/users/{name}")
def get_user(name:str):
    if name !="CyberX":
        raise UsersNotFound(name)
    return{
        "name":name
    }

    '''


'''

# global error handle(For this we have to import request from fastapi and from fastapi.responses import JSONResponse)
class UserNotFound(Exception):
    def __init__(self,name):
        self.name=name


@app.exception_handler(UserNotFound)
def user_not_found(request:Request,exc:UserNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "status":"error",
            "Message":f"user {exc.name} not found"
        }
    )

@app.get("/use/{name}")
def get_use(name:str):
    if name !="CyberX":
        raise UserNotFound(name)
    return{
        "name":name
    }
    
'''

'''

##### Dependency Injection #####
# we have to import Depends from fastapi

def get_data():
    return "Get data"

@app.get("/data")
def data(logic=Depends(get_data)):
    return logic

#reusable logic

def get_profile():
    return {
        "user":"Guest"
    }

@app.get("/profile")
def profile(name=Depends(get_profile)):
    return name

@app.get("/name")
def name(info=Depends(get_profile)):
    return info


# Auth example intro...

def verify_token(token:str=Header(None)):
    if token!= "CyberX":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return{
        "user":"You are a Authorized user",
        "name":"Krishna"
    }

@app.get("/Data_security")
def secure_data(user=Depends(verify_token)):
    return{
        "message":"Secure data accessed",
        "user":user
    } 
    '''  

####### MIDDLEWARE ########

'''
@app.middleware("http")
async def my_middleware(request:Request,call_next):
    print("Request Received")
    response=await call_next(request)
    print("Response sent")
    return response
'''
'''
@app.middleware("https")
async def log_middleware(request:Request,call_next):
    start_time=time.time()
    response= await call_next(request)
    process_time=time.time()-start_time
    print(f"Path:{request.url.path}| Time:{process_time}")
    return response
    '''

####### SQLite DATABASE #######

conn=sqlite3.connect("test.db",check_same_thread=False)
cursor=conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos(
    id INTEGER PRIMARY KEY,
    title STRING,
    COMPLETED STRING)
""")
conn.commit()

@app.get("/home")
def home():
    return "SQlite connected successfully"


