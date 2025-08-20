
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..models_extra import Preferences
from ..schemas_extra import PreferencesIn, PreferencesOut

try:
    from .auth import get_current_user  # type: ignore
except Exception:
    def get_current_user():
        raise RuntimeError("get_current_user not found; import from your auth module")

router = APIRouter(prefix="/prefs", tags=["preferences"])

def _get_or_create(db: Session, user_id: int) -> Preferences:
    pref = db.query(Preferences).filter(Preferences.user_id == user_id).first()
    if not pref:
        pref = Preferences(user_id=user_id)
        db.add(pref); db.commit(); db.refresh(pref)
    return pref

@router.get("", response_model=PreferencesOut)
def get_prefs(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return _get_or_create(db, user.id)

@router.put("", response_model=PreferencesOut)
def put_prefs(payload: PreferencesIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    pref = _get_or_create(db, user.id)
    pref.language = payload.language
    pref.email_notifications = payload.email_notifications
    pref.results_notifications = payload.results_notifications
    pref.reminders = payload.reminders
    db.add(pref); db.commit(); db.refresh(pref)
    return pref
