from services.models.outputs.auth.create_token_som import CreateTokenSOM


class CreateTokenMapper:
  @staticmethod
  def token_to_som(token: str) -> CreateTokenSOM:
    return CreateTokenSOM(token=token)
