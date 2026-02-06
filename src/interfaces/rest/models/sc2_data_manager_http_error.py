from pydantic import BaseModel


class SC2DataManagerHTTPError(BaseModel):
  message: str
