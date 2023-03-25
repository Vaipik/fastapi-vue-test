from typing import Optional

from pydantic import BaseModel


class UserAuthentication(BaseModel):
    email: str
    password: str


class UserProfile(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    sex_name: Optional[str]

