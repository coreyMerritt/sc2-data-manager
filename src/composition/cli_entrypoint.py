from composition.models.app_resources import AppResources
from composition.models.infrastructure_collection import InfrastructureCollection
from composition.models.repository_collection import RepositoryCollection
from composition.models.vars_collection import VarsCollection
from composition.resources import get_resources_dict
from composition.webserver.uvicorn_entrypoint import run_webserver
from interfaces.command_line.core.main import add_default_command, build_args, handle_args_routing


def entrypoint():
  resources = build_resources()
  add_default_command()
  args = build_args()
  handle_args_routing(
    args=args,
    logger=resources.infra.logger,
    config_parser=resources.infra.config_parser,
    cpu=resources.infra.cpu,
    database=resources.infra.database,
    disk=resources.infra.disk,
    environment=resources.infra.environment,
    memory=resources.infra.memory,
    run_webserver=run_webserver
  )

def build_resources() -> AppResources:
  resources_dict = get_resources_dict()
  infra = InfrastructureCollection(
    authenticator=resources_dict["infra"]["authenticator"],
    config_parser=resources_dict["infra"]["config_parser"],
    cpu=resources_dict["infra"]["cpu"],
    database=resources_dict["infra"]["database"],
    disk=resources_dict["infra"]["disk"],
    environment=resources_dict["infra"]["environment"],
    logger=resources_dict["infra"]["logger"],
    memory=resources_dict["infra"]["memory"],
    password_hasher=resources_dict["infra"]["password_hasher"],
    password_verifier=resources_dict["infra"]["password_verifier"],
    token_hasher=resources_dict["infra"]["token_hasher"],
    token_issuer=resources_dict["infra"]["token_issuer"]
  )
  repos = RepositoryCollection(
    user=resources_dict["repos"]["user"]
  )
  app_vars = VarsCollection(
    users_admin_secret=resources_dict["vars"]["users_admin_secret"]
  )
  resources = AppResources(
    infra=infra,
    repos=repos,
    vars=app_vars
  )
  return resources


if __name__ == "__main__":
  entrypoint()
