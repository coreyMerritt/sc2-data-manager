from domain.exceptions.repository_not_found_err import RepositoryNotFoundErr
from infrastructure.database.mappers.accounts import AccountsMapper
from infrastructure.database.mappers.build_orders import BuildOrdersMapper
from infrastructure.database.mappers.game_participants import GameParticipantsMapper
from infrastructure.database.mappers.game_summary import GameSummaryMapper
from infrastructure.database.mappers.graph_point_orms import GraphPointsMapper
from infrastructure.database.repositories.account_repository import AccountRepository
from infrastructure.database.repositories.game_summary_repository import GameSummaryRepository
from infrastructure.types.logger_interface import LoggerInterface
from services.base_service import BaseService
from services.exceptions.already_exists_err import AlreadyExistsErr
from services.mappers.game_summary.create_game_summary_mapper import CreateGameSummaryMapper


class GameSummaryManager(BaseService):
  _account_repository: AccountRepository
  _game_summary_repository: GameSummaryRepository

  def __init__(
    self,
    logger: LoggerInterface,
    account_repository: AccountRepository,
    game_summary_repository: GameSummaryRepository
  ):
    self._account_repository = account_repository
    self._game_summary_repository = game_summary_repository
    super().__init__(logger)

  def ingest_game_summary(self, game_summary_byte_string: bytes) -> None:
    self._logger.debug("Attempting ingest game summary...")
    try:
      game_summary = CreateGameSummaryMapper.byte_string_to_entity(
        byte_string=game_summary_byte_string
      )
      if self._game_summary_repository.exists(game_summary.filehash):
        raise AlreadyExistsErr
      account_orms = AccountsMapper.domain_to_orm(game_summary)
      build_order_orms = BuildOrdersMapper.domain_to_orm(game_summary)
      game_participant_orms = GameParticipantsMapper.domain_to_orm(game_summary)
      game_summary_orm = GameSummaryMapper.domain_to_orm(game_summary)
      player_owned_graph_points_orms = GraphPointsMapper.domain_to_orm(game_summary)
      for i in range(0, 2):
        try:
          account_orm = self._account_repository.get(account_orms[i].bnetid)
          if account_orms[i].name and not account_orm.name:
            account_orm.name = account_orms[i].name
        except RepositoryNotFoundErr:
          account_orm = account_orms[i]
        game_participant_orms[i].account = account_orm
        game_participant_orms[i].build_order = build_order_orms[i]
        game_participant_orms[i].graph_points = player_owned_graph_points_orms[i]
        game_summary_orm.game_participants = game_participant_orms
        for graph_points in player_owned_graph_points_orms[i]:
          graph_points.game_participant = game_participant_orms[i]
      self._game_summary_repository.create(game_summary_orm)
    except Exception as e:
      self._raise_service_exception(e)
    # create_user_som = CreateGameSummaryMapper.entity_to_som(created_user)
    # self._logger.debug(f"Successfully created user with ULID: {created_user.ulid}")
    # return create_user_som
