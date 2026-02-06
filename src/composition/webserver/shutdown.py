from fastapi import FastAPI


def shutdown(app: FastAPI) -> None:
  logger = app.state.resources.infra.logger
  logger.info("Shutting down...")
  app.state.resources.infra.database.dispose()
