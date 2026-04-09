
from pydantic import BaseModel, EmailStr, ValidationError, constr

class CreateUserPayload(BaseModel):
    username: EmailStr
    first_name: str
    last_name: str
    password: constr(min_length=4)
    class Config:
        extra = 'forbid'

class UpdateUserPayload(BaseModel):
    first_name: str
    last_name: str
    password: constr(min_length=4)
    class Config:
        extra = 'forbid'

#Fuction to validate the payload against given model
def is_valid_payload(payload, model):
    try:
        model(**payload)
        return True
    except ValidationError as e:
        print(e)    
        return False
