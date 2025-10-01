from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


# Admin model
class Admin(SQLModel, table=True):
    chat_id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    created_on: datetime = Field(default_factory=datetime.now)

# User model
class Lead(SQLModel, table=True):
    chat_id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    created_on: datetime = Field(default_factory=datetime.now)