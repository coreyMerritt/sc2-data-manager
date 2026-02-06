export log_path="/tmp/sc2-data-manager-exit-test.log"

function cleanup(){
  killServer
  rm -rf "$log_path"
}

function killServer() {
  pid=$(ss -lntp | awk -F 'pid=' '/:8000/ { split($2, a, ","); print a[1] }') || true
  if [[ -n "$pid" ]]; then
    kill "$pid"
  fi
}

function startServer() {
  killServer
  bash "./run-server.sh" > "$log_path" 2>&1 &
}