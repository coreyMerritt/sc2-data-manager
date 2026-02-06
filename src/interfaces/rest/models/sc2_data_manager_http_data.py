from pydantic import BaseModel


class SC2DataManagerHTTPData(BaseModel):
  model_config = {"extra": "allow"}
