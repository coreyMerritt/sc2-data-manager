#!/usr/bin/env python3
from _helpers import backup_db, require_sudo

if __name__ == "__main__":
  require_sudo()
  backup_db()
