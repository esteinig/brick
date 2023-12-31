FROM python:3.11-slim as builder

# Set the working directory in the builder stage
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --user -r requirements.txt

# Use another stage for the runner
FROM python:3.11-slim as runner

# Environment variable that determines API settings
ARG BRICK_ENV=

ARG UID=9234
ARG GID=9234
ARG USERNAME=brick-app

# Create a non-root user and switch to it
RUN groupadd -g ${GID} ${USERNAME} && useradd --no-log-init -u ${UID} -r -g ${USERNAME} ${USERNAME}
USER ${USERNAME}

WORKDIR /app

# Copy the locals directory into the new user home directory
COPY --chown=${USERNAME}:${USERNAME} --from=builder /root/.local/ /home/${USERNAME}/.local/

# Add user's local bin directory to PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

# Copy only the necessary files for Brick
COPY --chown=${USERNAME}:${USERNAME} pyproject.toml ./
COPY --chown=${USERNAME}:${USERNAME} brick/ ./brick/

# Install the brick package with the user dependencies from the builder stage
RUN pip install --no-cache-dir --user .

# Use other application code if necessary
COPY --chown=${USERNAME}:${USERNAME} tests ./tests/