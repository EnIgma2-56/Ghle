
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ---- Users ----
class UserOut(BaseModel):
    id: int
    identifier: str
    name: Optional[str] = None
    program: Optional[str] = None
    role: str
    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    identifier: Optional[str] = None
    program: Optional[str] = None

class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8)

# ---- Preferences ----
class PreferencesIn(BaseModel):
    language: str = "en"
    email_notifications: bool = True
    results_notifications: bool = True
    reminders: bool = True

class PreferencesOut(PreferencesIn):
    id: int
    user_id: int
    class Config:
        orm_mode = True

# ---- Contact ----
class ContactIn(BaseModel):
    name: str
    email: EmailStr
    message: str
