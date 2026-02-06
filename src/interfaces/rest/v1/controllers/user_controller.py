import asyncio

from fastapi import HTTPException, Request

from domain.enums.user_type import UserType
from domain.subdomain.entities.user import User
from interfaces.rest.models.sc2_data_manager_http_response import SC2DataManagerHTTPResponse
from interfaces.rest.v1.dto.req.user.create_user_req import CreateUserReq
from interfaces.rest.v1.dto.req.user.update_user_req import UpdateUserReq
from interfaces.rest.v1.mappers.user.create_user_mapper import CreateUserMapper
from interfaces.rest.v1.mappers.user.delete_user_mapper import DeleteUserMapper
from interfaces.rest.v1.mappers.user.get_user_mapper import GetUserMapper
from interfaces.rest.v1.mappers.user.update_user_mapper import UpdateUserMapper
from services.exceptions.item_creation_err import ItemCreationErr
from services.user_manager import UserManager


class UserController:
  async def get_user(self, req: Request, ulid: str) -> SC2DataManagerHTTPResponse:
    authenticated_user: User = req.state.user
    if (
      not getattr(req.state, "is_authenticated", False)
      or not getattr(req.state, "user", None)
      or authenticated_user.user_type not in (
        UserType.ADMIN,
        UserType.WRITE_CLIENT,
        UserType.READ_ONLY_CLIENT,
        UserType.STANDARD
      )
    ):
      raise HTTPException(
        status_code=401,
        detail="Permission denied",
      )
    if authenticated_user.user_type == UserType.STANDARD:
      if not authenticated_user.ulid == ulid:
        raise HTTPException(
          status_code=401,
          detail="Permission denied",
        )
    user_manager = UserManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    get_user_som = await asyncio.to_thread(user_manager.get_user, ulid)
    get_user_res = GetUserMapper.som_to_res(get_user_som)
    return SC2DataManagerHTTPResponse(
      data=get_user_res
    )

  async def create_user(self, req: Request, body: CreateUserReq) -> SC2DataManagerHTTPResponse:
    user_manager = UserManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    # If trying to create a privileged user, assert admin secret is present and correct
    if body.user_type in (UserType.ADMIN.value, UserType.READ_ONLY_CLIENT.value, UserType.WRITE_CLIENT.value):
      if not body.admin_secret:
        raise HTTPException(
          status_code=403,
          detail="Not permitted to create this item",
        )
      if not body.admin_secret == req.app.state.resources.vars.users_admin_secret:
        raise HTTPException(
          status_code=401,
          detail="Invalid admin secret",
        )
    create_user_service_model = CreateUserMapper.req_to_sim(body)
    create_user_som = await asyncio.to_thread(user_manager.create_user, create_user_service_model)
    if not create_user_som:
      raise ItemCreationErr()
    create_user_res = CreateUserMapper.som_to_res(create_user_som)
    return SC2DataManagerHTTPResponse(
      data=create_user_res
    )

  async def update_user(self, req: Request, body: UpdateUserReq) -> SC2DataManagerHTTPResponse:
    authenticated_user: User = req.state.user
    if (
      not getattr(req.state, "is_authenticated", False)
      or not getattr(req.state, "user", None)
      or authenticated_user.user_type not in (
        UserType.ADMIN,
        UserType.WRITE_CLIENT,
        UserType.STANDARD
      )
    ):
      raise HTTPException(
        status_code=401,
        detail="Permission denied",
      )
    if authenticated_user.user_type == UserType.STANDARD:
      if not authenticated_user.ulid == body.ulid:
        raise HTTPException(
          status_code=401,
          detail="Permission denied",
        )
    user_manager = UserManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    update_user_service_model = UpdateUserMapper.req_to_sim(body)
    update_user_som = await asyncio.to_thread(user_manager.update_user, update_user_service_model)
    if not update_user_som:
      raise ItemCreationErr()
    update_user_res = UpdateUserMapper.som_to_res(update_user_som)
    return SC2DataManagerHTTPResponse(
      data=update_user_res
    )

  async def delete_user(self, req: Request, ulid: str) -> SC2DataManagerHTTPResponse:
    authenticated_user: User = req.state.user
    if (
      not getattr(req.state, "is_authenticated", False)
      or not getattr(req.state, "user", None)
      or authenticated_user.user_type not in (
        UserType.ADMIN,
        UserType.WRITE_CLIENT
      )
    ):
      raise HTTPException(
        status_code=401,
        detail="Permission denied",
      )
    user_manager = UserManager(
      user_admin_secret=req.app.state.resources.vars.users_admin_secret,
      logger=req.app.state.resources.infra.logger,
      password_hasher=req.app.state.resources.infra.password_hasher,
      user_repository=req.app.state.resources.repos.user
    )
    delete_user_som = await asyncio.to_thread(user_manager.delete_user, ulid)
    delete_user_res = DeleteUserMapper.som_to_res(delete_user_som)
    return SC2DataManagerHTTPResponse(
      data=delete_user_res
    )
