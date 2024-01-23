set -e

# Secrets must be read from secret database env file as they
# can be exposed in Docker commands and configurations when
# configured directly in the container deployment


MONGO_INITDB_ROOT_USERNAME=$(cat /run/secrets/mongo_root_user)
MONGO_INITDB_ROOT_PASSWORD=$(cat /run/secrets/mongo_root_pwd)
BRICK_MONGODB_USERNAME=$(cat /run/secrets/brick_db_user)
BRICK_MONGODB_PASSWORD=$(cat /run/secrets/brick_db_pwd)

mongosh <<EOF
disableTelemetry()

use admin
db.createUser({
  user:  '$BRICK_MONGODB_USERNAME',
  pwd: '$BRICK_MONGODB_PASSWORD',
  roles: [
    {role: 'readWriteAnyDatabase', db: 'admin'},
    {role: 'dbAdminAnyDatabase', db: 'admin'}
  ]
})
EOF

# Remove last command from shell history
rm /data/db/.mongodb/mongosh/mongosh_repl_history
