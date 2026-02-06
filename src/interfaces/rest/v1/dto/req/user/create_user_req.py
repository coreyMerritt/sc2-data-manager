from pydantic import BaseModel, Field


class CreateUserReq(BaseModel):
  username: str = Field(..., min_length=4)
  email_address: str = Field(..., min_length=10)
  password: str = Field(..., min_length=8)
  user_type: str
  admin_secret: str | None = Field(default=None, min_length=4)
