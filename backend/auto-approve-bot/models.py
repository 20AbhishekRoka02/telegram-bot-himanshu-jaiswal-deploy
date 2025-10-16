from sqlmodel import Field, SQLModel, Relationship, Column
from datetime import datetime
import uuid
from sqlalchemy.dialects.mysql import JSON

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
    
# Message record
class MessageRecord(SQLModel, table=True):
    __tablename__ = "message_record"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    chat_id: str = Field(primary_key=True)
    message_id: str
    message: dict = Field(sa_column=Column(JSON))
    send_status: str
    sent_time: datetime = Field(default_factory=datetime.now)
    seen_time: datetime | None
    is_seen: bool = Field(default=False)