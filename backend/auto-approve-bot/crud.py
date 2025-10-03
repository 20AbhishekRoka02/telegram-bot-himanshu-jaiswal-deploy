from models import *
from sqlmodel import select, Session

# Create Lead
def createLead(engine: Session, lead: Lead):
    db_user = Lead(
        chat_id = lead.id,
        first_name = lead.first_name,
        last_name = lead.last_name,
        username = str(lead.username),
        is_premium= str(lead.is_premium),
        language_code = lead.language_code
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