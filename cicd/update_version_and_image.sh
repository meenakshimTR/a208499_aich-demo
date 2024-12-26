#!/bin/bash

current_dir=$(pwd)
if [ "$current_dir" != "python-app" ]; then
    cd python-app
fi

# Get the APP Release Version and Update
app_release_version=demo-python-$(yq eval '.appVersion' ./helm/chart/ach-backend/Chart.yaml)
echo "app release version: $app_release_version"
sed -i "s/appVersion/$app_release_version/" ./helm/chart/nonprod-values.yaml
cat ./helm/chart/nonprod-values.yaml

# Get the image_name with updated version
image_name=606349626084.dkr.ecr.us-east-1.amazonaws.com/${ECR_REPO}:$app_release_version
echo "image: $image_name"
sed -i "s|image-name|$image_name|" ./helm/chart/ach-backend/templates/deployment.yaml
cat ./helm/chart/ach-backend/templates/deployment.yaml

# Change the version for app.kubernetes.io/version
app_version=$(yq eval '.appVersion' ./helm/chart/ach-backend/Chart.yaml)
sed -i "s|appVersion|$app_version|g" ./helm/chart/ach-backend/templates/*.yaml