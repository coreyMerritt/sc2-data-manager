from fastapi import FastAPI

from interfaces.rest.health.routes import health_routes
from interfaces.rest.v1.routes import authentication_routes, game_summary_routes, user_routes


def register_routes(app: FastAPI) -> FastAPI:
  app.include_router(authentication_routes.router)
  app.include_router(game_summary_routes.router)
  app.include_router(health_routes.router)
  app.include_router(user_routes.router)
  return app
