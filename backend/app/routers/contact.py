
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models_extra import ContactMessage
from ..schemas_extra import ContactIn

router = APIRouter(prefix="/contact", tags=["contact"])

@router.post("")
def submit_contact(form: ContactIn, db: Session = Depends(get_db)):
    rec = ContactMessage(name=form.name, email=form.email, message=form.message)
    db.add(rec); db.commit()
    return {"message":"Received", "id": rec.id}
