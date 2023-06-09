from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean,text,ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import sqlalchemy as db

                    

Base = declarative_base()

class Participant(Base):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(255), nullable=True, unique=True)
    gender = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), nullable=True, unique=True)
    organization = db.Column(db.String(255), nullable=True)
    status = db.Column(Boolean, default=False, index=False)
    attend_by = db.Column(db.String(255), nullable=True)
    registration_time = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    event_id = db.Column(db.Integer, ForeignKey('events.id'))
    created_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP"))
    updated_at = db.Column(TIMESTAMP, nullable=False,server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    #event = relationship("Event", back_populates="participants")
    #attendance_id = db.Column(db.Integer, ForeignKey('attendances.id'))
