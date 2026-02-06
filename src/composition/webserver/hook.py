#!/usr/bin/env python3
import traceback

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from composition.webserver.register_exception_handlers import register_exception_handlers
from composition.webserver.register_middleware import register_middleware
from composition.webserver.register_routes import register_routes
from composition.webserver.register_signals import register_signals
from composition.webserver.shutdown import shutdown
from composition.webserver.startup import startup


def create_app() -> FastAPI:
  @asynccontextmanager
  async def lifespan(app: FastAPI):
    try:
      await startup(app)
      yield  # Application runs during this period
    except Exception as e:
      traceback.print_exc()
      raise e
    finally:
      shutdown(app)

  app = FastAPI()
  app = register_exception_handlers(app)
  app = register_middleware(app=app)
  app = register_routes(app)
  app = register_signals(app)
  app.router.lifespan_context = lifespan
  return app


if __name__ == "__main__":
  create_app()
