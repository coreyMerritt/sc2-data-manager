import uvicorn

from composition.resources import get_uvicorn_config


def run_webserver(
  host: str | None,
  port: int | None
) -> None:
  uvicorn_config = get_uvicorn_config()
  final_host = host if host else uvicorn_config.host
  final_port = port if port else uvicorn_config.port
  uvicorn.run(
    access_log=uvicorn_config.access_log,
    app=uvicorn_config.app,
    factory=uvicorn_config.factory,
    host=final_host,
    log_config=uvicorn_config.log_config,
    port=final_port,
    reload=uvicorn_config.reload,
    reload_excludes=uvicorn_config.reload_excludes,
    server_header=uvicorn_config.server_header
  )
