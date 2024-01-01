# Use an official Node runtime as a parent image
FROM node:20.9.0

# Set the working directory in the container to /app
WORKDIR /usr/src/app

# Copy the package.json and package-lock.json from the /app directory
COPY app/package*.json ./

# Install any needed packages
RUN npm install

# Bundle app source inside the Docker image
COPY app/ .

