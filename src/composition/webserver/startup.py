import asyncio

from fastapi import FastAPI

from composition.cli_entrypoint import build_resources


async def startup(app: FastAPI) -> None:
  resources = await asyncio.create_task(asyncio.to_thread(build_resources))
  app.state.resources = resources
  app.state.resources.infra.logger.info("Startup successful")
