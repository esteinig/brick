#!/bin/bash

# Navigate to your project directory
cd $2

# Depending on the environment, deploy the appropriate Docker Compose setup
if [ "$1" = "prod" ]; then

    # Pull down the production stack
    docker compose -f docker-compose.web.yml --profile prod --profile server --project-name prod down
    
    # Deploy with commit SHA passed into the script through action
    git checkout $3

    # Rebuild to include latest changes and up the stack again
    docker compose -f docker-compose.web.yml --profile prod --profile server --project-name prod up --build -d

    # Log this action
    echo "$date Successfully deployed production application" >> ~/brick_deploy_action.log

elif [ "$1" = "dev" ]; then

    # Pull down the development stack 
    docker compose -f docker-compose.web.yml --profile dev --profile server-dev --project-name dev down
    
    # Deploy with commit SHA passed into the script through action
    git checkout $3

    # Rebuild to include latest changes and up the stack again
    docker compose -f docker-compose.web.yml --profile dev --profile server-dev --project-name dev up --build -d

    # Log this action
    echo "$date Successfully deployed development application" >> ~/brick_deploy_action.log

else
    # Deployment script was run with invalid command-line input
    echo "$date Failed to run deploy script - $1 is not a valid option!" >> ~/brick_deploy_action.log
fi