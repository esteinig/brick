#!/bin/bash

# Navigate to your project directory
cd $2

# Depending on the environment, deploy the appropriate Docker Compose setup
if [ "$1" = "prod" ]; then
    # Pull down the production stack
    docker-compose -f docker-compose.web.yml --profile prod --profile server --project-name prod down
    
    # Make sure we are on `main` and pull latest stable changes
    # this is the latest release as this script is triggered
    # by the `cicd.yml` action workflow

    git checkout main 
    git pull origin main

    # Rebuild to include latest changes and up the stack again
    docker-compose -f docker-compose.web.yml --profile prod --profile server --project-name prod up --build -d

    # Log this action
    echo "$date Successfully deployed the production application" >> ~/brick_deploy_action.log

elif [ "$1" = "dev" ]; then
    # Pull down the development stack 
    docker-compose -f docker-compose.web.yml --profile dev --profile server-dev --project-name dev down
    
    # Make sure we are on `dev` and pull latest changes
    git checkout dev 
    git pull origin dev

    # Rebuild to include latest changes and up the stack again
    docker-compose -f docker-compose.web.yml --profile dev --profile server-dev --project-name dev up --build -d

    # Log this action
    echo "$date Successfully deployed the development application" >> ~/brick_deploy_action.log

else
    # Deployment script was run with invalid command-line input
    echo "$date Failed to run deploy script - `$2` is not a valid option!" >> ~/brick_deploy_action.log
fi