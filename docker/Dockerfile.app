# Use an official Node runtime as a parent image
FROM node:20.9.0 AS build

# Set the working directory in the container to /app
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json from the /app directory
COPY app/package*.json ./

# Install any needed packages
RUN npm install

# Bundle app source inside the Docker image
COPY app/ .

# Build the application
RUN npm run build

# Stage 2: Setup a lightweight production environment
FROM node:20.9.0-alpine

USER node

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY --chown=node:node app/package*.json ./

# Install only production dependencies
RUN npm install --production

# Copy built assets from the build stage
COPY --chown=node:node --from=build /usr/src/app/build build
COPY --chown=node:node --from=build /usr/src/app/node_modules node_modules
COPY --chown=node:node --from=build /usr/src/app/package.json package.json

# Set the node env vars required
ENV PORT=5173
ENV PROTOCOL_HEADER=x-forwarded-proto
ENV HOST_HEADER=x-forwarded-host


# Command to run 
CMD ["node", "build"]