from models import *
from sqlmodel import select, Session

# Create Lead
def createLead(engine: Session, lead: Lead):
    db_user = Lead(
        chat_id = lead.id,
        first_name = str(lead.first_name),
        last_name = str(lead.last_name),
        username = str(lead.username),
        is_premium= str(lead.is_premium),
        language_code = str(lead.language_code)
    )
    
    engine.add(db_user)
    engine.commit()
    engine.refresh(db_user)
    return db_user

# Get Lead by chat_id
def get_lead_by_chat_id(engine: Session, chat_id):
    statement = select(Lead).where(Lead.chat_id==str(chat_id))
    return { "user": engine.exec(statement = statement).first()}

# Get Admin by chat_id
# def get_admin_by_chat_id(engine: Session, chat_id):
#     statement = select(Admin).where(Admin.chat_id==str(chat_id))
#     return engine.exec(statement = statement).first()
    

# Get all leads
def getLeads(engine: Session):
    
    statement = select(Lead)
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:
        
        output_list.append({
            "id" : str(result.chat_id),
            "first_name":result.first_name,
            "last_name":result.last_name,
        })
    return output_list

# Update message record
def updateMessageRecord(engine: Session, chat_id: str, message_id: str, message: str, send_status: str, sent_time: datetime, is_seen: bool):
    statement = select(MessageRecord).where(MessageRecord.chat_id == chat_id)
    results = engine.exec(statement)
    # result = results.one()
    # print("results: ", dict(results))
    # print(len(results))
    
    
    # if result:
    #     print("One result is: ", result)
    # else:
    #     print("Not there! Need to record one.")
    
    try:
        result = results.one()
        # print(result)
        result.message_id=message_id
        result.message=message
        result.send_status=send_status
        sent_time=sent_time
        seen_time=None
        is_seen=is_seen
        
        engine.add(result)
        engine.commit()
        engine.refresh(result)
        return result
        
    except Exception as e:
        print(e)
        db_message = MessageRecord(
            chat_id = chat_id,
            message_id=message_id,
            message=message,
            send_status=send_status,
            sent_time=sent_time,
            seen_time=None,
            is_seen=False
        )
    
        engine.add(db_message)
        engine.commit()
        engine.refresh(db_message)
        return db_message
        
        
def updateMessageSeenRecord(engine: Session, chat_id: str, seen_time: datetime, is_seen: bool):
    statement = select(MessageRecord).where(MessageRecord.chat_id == chat_id)
    results = engine.exec(statement)
    result = results.one()
    
    result.seen_time = seen_time
    result.is_seen = is_seen
    
    engine.add(result)
    engine.commit()
    engine.refresh(result)
    return result