import asyncio
import signal
import sys
import threading

from fastapi import FastAPI


def register_signals(app: FastAPI) -> FastAPI:
  try:
    loop = asyncio.get_running_loop()
  except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
  stop_event = asyncio.Event()
  if sys.platform != "win32" and threading.current_thread() == threading.main_thread():
    try:
      loop.add_signal_handler(signal.SIGINT, stop_event.set)
      loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    except NotImplementedError:
      pass
  app.state.stop_event = stop_event
  return app
