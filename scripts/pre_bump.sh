#!/bin/sh
set -e

LATEST=$1
VERSION=$2


# Check that all commits
# comply with specifications
cog check

# Echo the version change
echo "bumping $LATEST to $VERSION"

# Replace docker-compose main script version
sed -i 's/PUBLIC_BRICK_VERSION='"$LATEST"'/PUBLIC_BRICK_VERSION='"$VERSION"'/' docker/brick.env

# Replace Python package version line
sed -i 's/version = "'"${LATEST}"'"/version = "'"${VERSION}"'"/' pyproject.toml

# Replace Sveltekit application version
# `npm install` or `build` in the container will update the `package-lock.json`
sed -i 's/"version": "'"${LATEST}"'"/"version": "'"${VERSION}"'"/' app/package.json
