from interfaces.rest.models.sc2_data_manager_http_data import SC2DataManagerHTTPData


class DeleteUserRes(SC2DataManagerHTTPData):
  ulid: str
  username: str
  email_address: str
  user_type: str
