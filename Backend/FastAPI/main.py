from fastapi import FastAPI

app = FastAPI() # starting context

@app.get("/") # get request @server will recieve this text --> The root is localhost
async def root():
    return "¡Hola FastAPI!"

@app.get("/url")
async def url(): # useful names will describe what functions do
    return { "url": "https://mouredev.com/python" }

'''
lanzo con:
    uvicorn main:app --reload
    donde:
        app es el contexto inicial
        main es el nombre del fichero


para ver la documentación automáticamente generada tengo 2 opciones:
    http://127.0.0.1:8000/docs
    http://127.0.0.1:8000/redoc
    
'''