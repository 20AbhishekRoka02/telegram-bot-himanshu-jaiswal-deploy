# from .models import Admin
from pydantic import EmailStr
from pydantic import BaseModel, Field, EmailStr, constr, condecimal

# class AdminLogin(Admin):
#     email: EmailStr
#     password: str

# Login Schema
class LoginUser(BaseModel):
    email : EmailStr
    password : str
    role : str

# Update Admin
class UpdateAdmin(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    password: str

# Delete Admin
class DeleteAdmin(UpdateAdmin):
    pass
    