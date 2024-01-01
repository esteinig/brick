FROM condaforge/mambaforge:latest as builder

# Set the working directory in the builder stage
WORKDIR /app

# Create a new environment with Python 3.11
RUN mamba create -n brick -c bioconda blast python=3.11 --yes

# Activate the new environment
SHELL ["conda", "run", "-n", "brick", "/bin/bash", "-c"]

# Copy the requirements file
COPY requirements.txt ./

# Install dependencies from requirements.txt
RUN mamba install --file requirements.txt --yes \
    && mamba clean --all --yes

# Use another stage for the runner
FROM condaforge/mambaforge:latest as runner

# Environment variable that determines API settings
ARG BRICK_ENV=

ARG UID=9234
ARG GID=9234
ARG USERNAME=brick-app

# Create a non-root user and switch to it
RUN groupadd -g ${GID} ${USERNAME} && useradd --no-log-init -u ${UID} -r -g ${USERNAME} ${USERNAME}
USER ${USERNAME}

WORKDIR /app

# Copy the conda environment from the builder stage
COPY --chown=${USERNAME}:${USERNAME} --from=builder /opt/conda /opt/conda

# Set the environment variables to use the conda environment
ENV PATH=/opt/conda/envs/brick/bin:$PATH

# Copy only the necessary files for Brick
COPY --chown=${USERNAME}:${USERNAME} pyproject.toml ./
COPY --chown=${USERNAME}:${USERNAME} brick/ ./brick/

# Install the brick package with the user dependencies from the builder stage
RUN pip install --no-dependencies --no-cache .

# Use other application code if necessary
COPY --chown=${USERNAME}:${USERNAME} tests ./tests/