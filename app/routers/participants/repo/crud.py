from fastapi import status
from routers.participants.schemas import participants
from models.models import Event,Participant
from utils.database import Database
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from mail import sendmail





database = Database()
engine = database.get_db_connection()
session = database.get_db_session(engine)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")









async def add_participants(participantRequest: participants.ParticipantRequest):

    email_query = session.query(Participant).filter(
        Participant.email == participantRequest.email).first()
    
    phone_query = session.query(Participant).filter(
        Participant.phone_number == participantRequest.phone_number).first()

    if email_query or phone_query:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER,
           detail=f"Participant with email or phone number already exists")


    new_participant = Participant()
    new_participant.name = participantRequest.name
    new_participant.phone_number = participantRequest.phone_number
    new_participant.gender = participantRequest.gender
    new_participant.email = participantRequest.email
    new_participant.organization = participantRequest.organization
    new_participant.attend_by = participantRequest.attend_by
    new_participant.registration_time = participantRequest.registration_time
    new_participant.location = participantRequest.location
    new_participant.event_id = participantRequest.event_id
    new_participant.status = 0
    
    session.add(new_participant)
    session.flush()
    session.refresh(new_participant, attribute_names=['id'])
    #await sendmail.sendEmailToNewParticipant([new_participant.email], new_participant)
    data = {
        "phone_number": new_participant.phone_number,
        "email": new_participant.email,
        "status": new_participant.status,
        "registration_time": new_participant.registration_time,
        "event_id": new_participant.event_id,
        "gender": new_participant.gender,
        "name": new_participant.name,
        "organization": new_participant.organization,
        "attend_by": new_participant.attend_by,
        "location": new_participant.location
    }
    session.commit()
    session.close()
    return data






async def all_Participant():
    data = session.query(Participant).all()
    return data






async def get_Participant_By_Id(id: int):
    data = session.query(Participant).filter(Participant.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with the id (" + str(id) + ") is not found")
    return data
    









async def updateParticipant(updateParticipant: participants.UpdateParticipant):
    participant_id = updateParticipant.id
    is_Participant_update = session.query(Participant).filter(Participant.id == participant_id).update({
            Participant.name: updateParticipant.name,
            Participant.phone_number: updateParticipant.phone_number,
            Participant.gender: updateParticipant.gender,
            Participant.email: updateParticipant.email,
            Participant.organization: updateParticipant.organization,
            Participant.attend_by: updateParticipant.attend_by,
            Participant.registration_time: updateParticipant.registration_time,
            Participant.location: updateParticipant.location,
            Participant.event_id: updateParticipant.event_id,
            Participant.status: 1
        }, synchronize_session=False)
    session.flush()
    session.commit()
    if not is_Participant_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participant with the id (" + str(participant_id) + ") is not found")

    data = session.query(Participant).filter(Participant.id == participant_id).one()
    return data











async def phone_number_email(phone_number_email: str):
    if "@" in phone_number_email:
        participant = session.query(Participant).filter(
            Participant.email == phone_number_email).first()
    else:
        participant = session.query(Participant).filter(
            Participant.phone_number == phone_number_email).first()
    return participant





    






async def get_Participant_By_attend_by(attend_by: str):
    data = session.query(Participant).filter(
            Participant.attend_by == attend_by).all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attend by (" + str(attend_by) + ") is not available")
    elif attend_by == "virtual":
            data = session.query(Participant).filter(Participant.attend_by == attend_by).all()
    elif attend_by == "onsite":
            data = session.query(Participant).filter(Participant.attend_by == attend_by).all()
    return data









async def deleteParticipant(id: str):
    db_data = session.query(Participant).filter(Participant.id == id).update({
            Participant.status: 0
            }, synchronize_session=False)
    session.flush()
    session.commit()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Participant with the id (" + str(id) + ") is not available")

    data = session.query(Participant).filter(Participant.id == id).one()
    return data








async def show_participant_event_all(id: int):
    data = session.query(Participant).filter(
            Participant.event_id == Event.id).filter(Event.id == id).all()
    
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Participant with the id {id} is not available")
    return data









async def count_all_Participant():
    data = session.query(Participant).count()
    return data






async def count_all_Participant_Confirm():
    data = session.query(Participant).filter(Participant.status == 1).count()
    return data







async def count_all_Participant_Not_Confirm():
    data = session.query(Participant).filter(Participant.status == 0).count()
    return data





