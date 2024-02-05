from fastapi import APIRouter, HTTPException

# to work with objects I need this, optherwise I work with plain JSON
from pydantic import BaseModel 

# lauch: uvicorn users:router --reload
router = APIRouter()



# Entity User - every entity wich implements BaseModel can be handled like a JSON object
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int



users_list = [
    User(id=1, name="Jose", surname="Mora", url="https://github.com/JoseMoraDev", age=38),
    User(id=2, name="Miriam", surname="Durán", url="https://github.com/AnnieAmrod", age=28),
    User(id=3, name="Gabriel", surname="Vargas", url="https://github.com/GabrielCrackPro", age=22)
]



#plain JSON option - unused
@router.get("/users2")
async def usersjson():
    return [
        {"name": "Jose", "surname": "Mora", "url": "https://github.com/JoseMoraDev", "age": 38},
        {"name": "Miriam", "surname": "Durán", "url": "https://github.com/AnnieAmrod", "age": 28},
        {"name": "Gabriel", "surname": "Vargas", "url": "https://github.com/GabrielCrackPro", "age": 22}
    ]



# class option - best choice
@router.get("/users") # http://127.0.0.1:8000/users
async def users():
    return users_list
    #* return User(name="Jose", surname="Mora", url="https://github.com/JoseMoraDev", age=38)



# like beofre, but with id at url path
@router.get("/user/{id}") # http://127.0.0.1:8000/user/1
async def user(id: int):
    return search_user(id)



'''
    return list(users) is not a right choice because returns this:

        [
            {
                "id": 1,
                "name": "Jose",
                "surname": "Mora",
                "url": "https://github.com/JoseMoraDev",
                "age": 38
            }
        ]

    A list... I need one user only, that's why I use return list(users)[0] instead of return list(users)

'''



# query option means 'key=value' at url path
@router.get("/userquery/") # http://127.0.0.1:8000/userquery/?id=1
async def user(id: int):
    return search_user(id)



'''
@router.get("/userquery/")
async def user(id: int):
    print(id)
    users = filter(lambda user: user.id == id, users_list)
    print(users)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}

'''



# outsourcing the user search function
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}



#! create user
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(204, detail="The user already exists")
        # return { "error": "The user already exists"}
    users_list.append(user)
    return "User created!"
        # return was replaced by raise & HTTPException
        # HTTPException is never thrown with return, but always with raise
            # that's because raise spreads the exception, not only returns it
        # detail
            # success messages won't show detail
            # error messages will show detail



#! update user
@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "the user was not created"}
    return user



#! delete user
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            users_list[index] = user
            del users_list[index]
            found = True
    if not found:
        return {"error": "The user was not deleted"}
    return "User deleted"



'''
status codes

    all:
        https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    
    most used in FastAPI
        https://fastapi.tiangolo.com/tutorial/response-status-code/?h=used+codes#about-http-status-codes
    
    it's a good practice to use the standard codes instead of text messages

'''