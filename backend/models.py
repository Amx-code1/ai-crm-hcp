# from sqlalchemy import Column, Integer, String, Text
# from db import Base

# class Interaction(Base):
#     __tablename__ = "interactions"

#     id = Column(Integer, primary_key=True, index=True)
#     hcp_name = Column(String)
#     notes = Column(Text)
#     sentiment = Column(String)
#     follow_up = Column(String)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()


# 🔹 SQLAlchemy model (DB table)
class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String)
    notes = Column(String)
    sentiment = Column(String)
    follow_up = Column(String)


# 🔹 Pydantic models (API / tools)
class EditInteraction(BaseModel):
    id: int
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    sentiment: Optional[str] = None
    notes: Optional[str] = None
    follow_up: Optional[str] = None


class ChatRequest(BaseModel):
    message: str