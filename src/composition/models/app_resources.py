from dataclasses import dataclass

from composition.models.infrastructure_collection import InfrastructureCollection
from composition.models.repository_collection import RepositoryCollection
from composition.models.vars_collection import VarsCollection


@dataclass
class AppResources:
  infra: InfrastructureCollection
  repos: RepositoryCollection
  vars: VarsCollection
