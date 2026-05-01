from langchain.tools import tool
from db import SessionLocal
from models import Interaction
from models import EditInteraction

db = SessionLocal()

def get_last_interaction_id():
    db = SessionLocal()
    last = db.query(Interaction).order_by(Interaction.id.desc()).first()
    return last.id if last else None

@tool
def log_interaction(data: dict):
    """Log a new HCP interaction into the database."""

    db = SessionLocal()

    obj = Interaction(
        hcp_name=data.get("hcp_name"),
        notes=data.get("notes"),
        sentiment=data.get("sentiment"),
        follow_up=data.get("follow_up")
    )

    db.add(obj)
    db.commit()    
    db.refresh(obj)  

    return {"status": "logged"}


@tool
def edit_interaction(data: EditInteraction):
    """Edit an existing interaction by ID."""

    db = SessionLocal()

    obj = db.query(Interaction).filter(Interaction.id == data.id).first()

    if not obj:
        return {"error": "Interaction not found"}

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        if key != "id" and value is not None:
            setattr(obj, key, value)

    db.commit()

    return {"status": "updated"}

@tool
def fetch_interactions(_=None):
    """Fetch all stored HCP interactions."""

    db = SessionLocal()

    interactions = db.query(Interaction).order_by(Interaction.id.desc()).all()

    
    return [
    f"{i.hcp_name} | {i.notes} | {i.sentiment}" +
    (f" | Follow-up: {i.follow_up}" if i.follow_up else "")
    for i in interactions
]
    

@tool
def suggest_next_action(text: str):
    """Suggest next action based on interaction notes."""
    
    if "not interested" in text.lower():
        return "Try re-engaging after a few weeks with new product updates"
    
    return "Follow up in next visit"


@tool
def summarize_hcp(data):
    """Summarize HCP engagement based on interactions."""

    
    if isinstance(data, list):
        interactions = data
    elif isinstance(data, dict):
        interactions = data.get("data", [])
    else:
        interactions = []

    return f"HCP has {len(interactions)} interactions"