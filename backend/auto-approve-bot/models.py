from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


# Admin model
# class Admin(SQLModel, table=True):
#     chat_id: str = Field(primary_key=True)
#     first_name: str
#     last_name: str
#     created_on: datetime = Field(default_factory=datetime.now)

# User model
class Lead(SQLModel, table=True):
    __tablename__="leads"
    chat_id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    username: str
    is_premium: str # because there is problem with is_premium being bool, as it is returning None
    language_code: str
    joined_on: datetime = Field(default_factory=datetime.now)
    
