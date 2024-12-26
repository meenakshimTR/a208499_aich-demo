#!/usr/bin/env bash
# This script is used to deploy cloudformation for ECR repo that will be used to push container image.
set -e
set -x

ASSET_ID=208499
RESOURCE_OWNER="AICHDevopsEngineeringGroup@thomsonreuters.com"
ENVIRONMENT_TYPE="PRE-PRODUCTION"
STACK_NAME_BACKEND_SUFFIX=demo
STACK_BACKEND_NAME=a${ASSET_ID}-${STACK_NAME_BACKEND_SUFFIX}
TEMPLATE_FILENAME="ecr.yaml"
BACKEND_SERVICE=demo
CICD_ACCOUNT_ID="606349626084"
PLEXUS_ACCOUNT_ID="674700511554"
PROFILE="tr-sharedcap-cicd-prod"
REGION="us-east-1"

aws cloudformation deploy --template-file ${TEMPLATE_FILENAME} \
  --stack-name ${STACK_BACKEND_NAME} \
  --parameter-overrides \
    "AssetId=${ASSET_ID}" \
    "ServiceName=${BACKEND_SERVICE}" \
    "CicdAccountId=${CICD_ACCOUNT_ID}" \
    "PlexusAccountId=${PLEXUS_ACCOUNT_ID}" \
  --tags \
    "tr:application-asset-insight-id=${ASSET_ID}" \
    "tr:environment-type=${ENVIRONMENT_TYPE}" \
    "tr:resource-owner=${RESOURCE_OWNER}" \
    "Name=${STACK_NAME_BACKEND_SUFFIX}" \
  --profile ${PROFILE} \
  --region ${REGION}