from domain.enums.user_type import UserType
from domain.subdomain.entities.user import User
from infrastructure.database.orm.user_orm import UserORM


class UserMapper:
  @staticmethod
  def domain_to_orm(user: User) -> UserORM:
    return UserORM(
      ulid=user.ulid,
      username=user.username,
      email_address=user.email_address,
      password_hash=user.password_hash,
      user_type=user.user_type.value,
      email_verified=user.email_verified,
      created_at=user.created_at,
      disabled_at=user.disabled_at
    )

  @staticmethod
  def orm_to_domain(user_orm: UserORM) -> User:
    return User(
      ulid=user_orm.ulid,
      username=user_orm.username,
      email_address=user_orm.email_address,
      password_hash=user_orm.password_hash,
      user_type=UserType(user_orm.user_type),
      email_verified=user_orm.email_verified,
      created_at=user_orm.created_at,
      disabled_at=user_orm.disabled_at
    )
