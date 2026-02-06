FROM rockylinux:9.3

SHELL ["/bin/bash", "-c"]
WORKDIR /app

# Build Args
ARG SC2_DATA_MANAGER_DEPLOYMENT_ENVIRONMENT
ARG SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR
ARG SC2_DATA_MANAGER_MODEL_CONFIG_DIR

# Validate Build Args that don't have a default
RUN [[ -n "$SC2_DATA_MANAGER_DEPLOYMENT_ENVIRONMENT" ]] || { echo "ERROR: SC2_DATA_MANAGER_DEPLOYMENT_ENVIRONMENT build arg is required" && exit 1; }
RUN [[ -n "$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR" ]] || { echo "ERROR: SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR build arg is required" && exit 1; }
RUN [[ -n "$SC2_DATA_MANAGER_MODEL_CONFIG_DIR" ]] || { echo "ERROR: SC2_DATA_MANAGER_MODEL_CONFIG_DIR build arg is required" && exit 1; }

# Export Build Args
ENV SC2_DATA_MANAGER_DEPLOYMENT_ENVIRONMENT="$SC2_DATA_MANAGER_DEPLOYMENT_ENVIRONMENT"
ENV SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR="$SC2_DATA_MANAGER_GLOBAL_CONFIG_DIR"
ENV SC2_DATA_MANAGER_MODEL_CONFIG_DIR="$SC2_DATA_MANAGER_MODEL_CONFIG_DIR"

COPY "." "/app/"

RUN rm -rf "./.env"

RUN dnf update -y
RUN dnf install -y \
  python3.11 \
  python3.11-pip \
  sudo
RUN dnf install -y \
  gcc
RUN dnf install -y \
  jq \
  libpq-devel \
  postgresql-devel
RUN dnf clean all

RUN ln -sf /usr/bin/python3.11 /usr/bin/python3 &&\
  ln -sf /usr/bin/pip3.11 /usr/bin/pip3 &&\
  ln -sf /usr/bin/python3.11 /usr/bin/python && \
  ln -sf /usr/bin/pip3.11 /usr/bin/pip

RUN ./install.sh ${SC2_DATA_MANAGER_DEPLOYMENT_ENVIRONMENT}

ENTRYPOINT ["./run-server.sh"]
