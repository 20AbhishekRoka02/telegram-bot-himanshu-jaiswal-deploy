from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime




# User model
class User(SQLModel, table=True):
    chat_id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    created_on: datetime = Field(default_factory=datetime.now)
    
    
