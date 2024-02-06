from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # auth module import
    # OAuth2PasswordBearer - manages auth, user and password
    # OAuth2PasswordRequestForm - manages password auth requests in FastAPI



app = FastAPI() # app instance



oauth2 = OAuth2PasswordBearer(tokenUrl="login") # instance of auth system



class User(BaseModel):

    username: str
    fullname: str
    email: str
    disabled: bool



class UserDB(User): # inherits User attributes

    password: str



users_db = {

    "josemoradev": 
        {
            "username": "josemoradev",
            "fullname": "Jose Antonio Mora González",
            "email": "86jamg@gmail.com",
            "disabled": False,
            "password": "1234"
        },

    "Annie_Ämrod": 
        {
            "username": "miriam_duran",
            "fullname": "Miriam Durán García",
            "email": "example@gmail.com",
            "disabled": False,
            "password": "4321"
        },
}



def search_user(username: str):

    if username in users_db:
        return UserDB(**users_db[username]) 
    
'''
    returns Object UserDB from database users_db, but only the user which username is equal to username parameter in search_user function
    
    dict key names must match the parameter names of the UserDB function

    This is useful to pass a dictionary as arguments to a function that expects keyword parameters, and the dictionary already has the necessary keys with the correct values, whose match function keys
'''



def search_user_db(username: str):

    if username in users_db:
        return User(**users_db[username]) 



async def current_user(token: str = Depends(oauth2)): # depends of token: oauth2

    user =  search_user_db(token)

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Invalid auth credentials",
            headers = { "WWW-Authenticate": "Bearer" }
        )
    
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Inactive user'
        )
    
    return user



@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): # depends means it recieves data but it's not depending of no one/nothing

    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(
            status_code=400, detail="Invalid username"
        )
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="Wrong password"
        )
    
    return {"access_token": user.username, "token_type": "bearer"}
        # a real encrypted token is used instead of user.username



@app.get("/users/me")
async def me(user: User = Depends(current_user)): # strong user validation

    return user



'''
    api calls

        url: http://127.0.0.1:8000/login
        append body > form, fields username & password and it's values


        http://127.0.0.1:8000/users/me
        get method, auth > bearer, bearer token 'josemoradev'

'''