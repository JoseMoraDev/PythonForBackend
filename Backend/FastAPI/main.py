from fastapi import FastAPI
from routers import products # accessing products file
from routers import users
from fastapi.staticfiles import StaticFiles



app = FastAPI() # starting context



#! routers imports
app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
    #app.mount("/expositionURL"), StaticFiles(directory="directoryKind=static"), name="expositionName")
    # type http://127.0.0.1:8000/static/images/python.jpg at browser to see the jpg file




@app.get("/") # get request @server will recieve this text --> The root is localhost
async def root():
    return "Hello FastAPI!"



@app.get("/url")
async def url(): # useful names will describe what functions do
    return { "url": "https://mouredev.com/python" }



'''
lauch command:
    uvicorn main:app --reload
    where:
        app - initial context
        main - filename

to see autodocs selfgenerated I have two options:
    http://127.0.0.1:8000/docs
    http://127.0.0.1:8000/redoc
    
'''