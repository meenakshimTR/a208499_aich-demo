#!/usr/bin/env python3
# This script publishes images to Docker to the accounts and regions
# mentioned in the deploy spec.
# It then sets the defined param (from --param-path) to the image URL for the give environment.
#
# Usage:
# python3 bake_helper.py --image <IMAGE_NAME> --tag <TAG> --param-path <PARAM_PATH>
#
# Example:
# python3 bake_helper.py --image my-docker-image --tag 1444 --param-path DeployerParameters.Helm.SetValues.image_url
#
# Requirements:
# boto3 docker pyyaml

import argparse
import base64
import pathlib

import boto3
import docker
import yaml

parser = argparse.ArgumentParser("Publish Docker images and update the deploy spec.")
parser.add_argument("--image", nargs=1, required=True)
parser.add_argument("--tag", nargs=1, required=True)
parser.add_argument("--param-path", nargs=1, required=True)
args = parser.parse_args()

docker_client = docker.from_env()
image_name = args.image[0]
tag = args.tag[0]
update_path = args.param_path[0].split(".")

print("Docker Client:",docker_client)
print("Image Name:", image_name)
print("Image tag:", tag)
print("Deployspec Update Path:", update_path)

# Function for setting values deep in a dict even if some parts are missing
def deepset(dict_, item, *path):
    for key in path[:-1]:
        dict_ = dict_.setdefault(key, {})
    dict_[path[-1]] = item


def assume_role(role_arn, region_name=None, session_name=None, time=900):
    """
    Create a new session based on the given role.
    """
    sts = boto3.client("sts")
    session_name = session_name or "CumulusAssumedRole"
    credentials = sts.assume_role(
        RoleArn=role_arn, RoleSessionName=session_name, DurationSeconds=time,
    )
    credentials = credentials["Credentials"]
    return boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"],
        region_name=region_name,
    )


def get_ecr_client(asset_id, account, region):
    """
    Return a client(Poweruser2) with which to enable ecr scanning.
    """
    power_user_arn = f"arn:aws:iam::{account}:role/human-role/a{asset_id}-PowerUser2"
    assumed_session = assume_role(
        role_arn=power_user_arn,
        region_name=region,
        session_name="EcrScanning",
        time=15 * 60,  # 15 minutes - Minimum time for session
    )
    return assumed_session.client("ecr")


# Load deployspec
deployspec_nonprod_file = pathlib.Path("cicd/cumulus-deployspec.yaml")
deployspec_nonprod = yaml.safe_load(deployspec_nonprod_file.read_text())

# Push image to all environments (regions & accounts)
defaults = deployspec_nonprod["Defaults"]
for env, env_values in deployspec_nonprod.items():
    if env == "Defaults":
        continue
    if env_values.get("ScriptOnlyLambdas"):
        continue
    env_acc = env_values.get("AccountId", defaults.get("AccountId"))
    env_region = env_values.get("AccountRegion", defaults.get("AccountRegion"))
    asset_id = env_values.get("AssetId", defaults.get("AssetId"))

    # Log in to relevant ECR for account+region
    ecr = boto3.client("ecr", region_name=env_region)
    resp = ecr.get_authorization_token(registryIds=[env_acc])["authorizationData"][0]
    token = base64.decodebytes(resp["authorizationToken"].encode()).decode()
    [username, password] = token.split(":")
    registry = resp["proxyEndpoint"]
    docker_client.login(username, password, registry=registry)

    # Tag and push image
    registry = registry.replace("https://", "", 1)
    print("Docker Registry:", registry)

    image_uri = f"{registry}/{image_name}"
    docker_client.images.get(image_name).tag(image_uri, tag=tag)
    image_uri = f"{image_uri}:{tag}"
    print("Image URI", image_uri)

    for line in docker_client.images.push(image_uri, stream=True, decode=True):
        print(line)
        if "error" in line.keys():
            raise ValueError("An error occurred when pushing the image.")
    deepset(env_values, tag, *update_path)

    # Manual start image scan
    ecr_client = get_ecr_client(asset_id, env_acc, env_region)
    ecr_client.start_image_scan(
        repositoryName=image_name, imageId={"imageTag": str(tag)}
    )

deployspec_nonprod_file.write_text(yaml.dump(deployspec_nonprod))