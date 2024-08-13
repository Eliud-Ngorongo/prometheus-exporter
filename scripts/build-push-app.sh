#!/bin/bash

# WARNING: Do not edit this file

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname "$SCRIPT"`

. "${SCRIPTPATH}/../settings.sh"
. "${SCRIPTPATH}/_library.sh"

set -e

APP_DIR="${SCRIPTPATH}/../app-${APP_LANGUAGE}"

log_test "Applying code formatter to your app code"
make -C "${APP_DIR}" fmt && log_pass "Autoformatted successfully" || ( log_warn "Could not autoformat the code" )

log_test "Running linter for your Dockerfile"
make -C "${APP_DIR}" dockerfile-lint && log_pass "Dockerfile lint check passed" || ( log_warn "Dockerfile lint check did not pass" )

log_test "Building Docker image of your app"
echo make -C "${APP_DIR}" build CLUSTER="${CLUSTER_NAME}"
make -C "${APP_DIR}" build && log_pass "Build and tagged successfully" || ( log_fail "Could not build and tag docker image" ; exit 1 )

log_test "Pushing Docker image of your app to local kind registry"
make -C "${APP_DIR}" push CLUSTER="${CLUSTER_NAME}" && log_pass "Pushed successfully" || ( log_fail "Could not push docker image" ; exit 1 )
