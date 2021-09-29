from fastapi import FastAPI,HTTPException, Request, status
from pydantic import BaseModel, ValidationError, errors, validator, StrictStr,Field
from pydantic.error_wrappers import error_dict
from pydantic.types import StrictInt
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.types import Message
app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    # print(exc)
    # return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
    return JSONResponse(
        # status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        # content=jsonable_encoder({"detail": exc.errors(), "Error": "Rollno is not integer"}),
        content=jsonable_encoder({"error": "valueError" , "errorDescription": exc.detail}),
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # print(list[exc.errors()])
    # a = exc.errors['errors']['msg']
    # print(a)
    for dictionary in [exc.errors()]:
       err = dictionary[0]['type']
       err_msg = dictionary[0]['msg']
    #    print(err)
    #    print(err_msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        # content=jsonable_encoder({"detail": exc.errors(), "Error": "Rollno is not integer"}),
        content=jsonable_encoder({"error": err , "errorDescription": err_msg}),
    )
  

class UserModel(BaseModel):
    Name: StrictStr
    rollNo: StrictInt

    

    @validator('Name')
    def name_must_not_be_emptyString(cls, v):
        if v == '':
            raise HTTPException(status_code=422, detail='Name cannot be empty string')
        if v == ' ':
            raise HTTPException(status_code=422, detail='Name is invalid')
        if v.replace(" ", "").isalpha() == False:
            raise HTTPException(status_code=422, detail='Name is invalid')
        
        return v

    




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login", response_model=UserModel)
async def login(user : UserModel):
    print(user)
    
    return user