from pydantic import BaseModel


class CreateTokenRes(BaseModel):
  token: str
