from pydantic import BaseModel, Field


class UpdateUserReq(BaseModel):
  ulid: str
  username: str
  email_address: str
  email_verified: bool
  disabled: bool
  user_type: str
  admin_secret: str | None = Field(default=None, min_length=4)
