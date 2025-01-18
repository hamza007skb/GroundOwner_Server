from pydantic import BaseModel


class OwnerSignUpModel(BaseModel):
    name: str
    email: str
    password: str
    phone_no: str = '123456789'
    verified_by: str = 'sameer@gmail.com'

