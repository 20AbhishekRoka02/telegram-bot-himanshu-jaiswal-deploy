from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime




# User model
class Lead(SQLModel, table=True):
    chat_id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    created_on: datetime = Field(default_factory=datetime.now)