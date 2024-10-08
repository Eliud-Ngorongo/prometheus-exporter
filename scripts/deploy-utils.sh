#!/bin/bash

# WARNING: Do not edit this file

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname "$SCRIPT"`

. "${SCRIPTPATH}/../settings.sh"
. "${SCRIPTPATH}/_library.sh"

set -eu

switch_k8s_context
apply_manifests utils.yml "Deploying utils for test framework"
wait_for_curl || log_fail "Couldn't get curl utils to start"
