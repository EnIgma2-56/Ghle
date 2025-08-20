
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas_extra import UserOut, UserUpdate, ChangePasswordRequest
from ..security import verify_password, hash_password

# We expect you already have a dependency to get the current user object.
# Import it from your existing auth router/module:
try:
    from .auth import get_current_user  # type: ignore
except Exception:
    # Fallback no-op to help import; replace with your real dependency.
    def get_current_user():
        raise HTTPException(status_code=500, detail="get_current_user dependency not found")

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserOut)
def read_me(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return user

@router.put("/me", response_model=UserOut)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    updated = False
    if payload.name is not None:
        user.name = payload.name; updated = True
    if payload.identifier is not None:
        user.identifier = payload.identifier; updated = True
    if hasattr(user, "program") and payload.program is not None:
        user.program = payload.program; updated = True
    if updated:
        db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/change-password")
def change_password(req: ChangePasswordRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not verify_password(req.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    user.password_hash = hash_password(req.new_password)
    db.add(user); db.commit()
    return {"message":"Password updated"}
