# ITI110 project iti110_tbc 

## Deployment
1. Resource Group: <RESOURCE_GROUP>
2. Image Registry: <IMAGE_REGISTRY>
3. Resource Plan: <RESOURCE_PLAN>
4. App Service Name: <APP_NAME>
5. Docker Registry URL: <IMAGE_REGISTRY_URL>
6. Docker Image Name: <IMAGE_NAME>

Typical Image tag: <IMAGE_REGISTRY_URL>/<IMAGE_REPO>:<VERSION>

### Azure Resource Group setup
az group create --name <RESOURCE_GROUP> --location eastus

### Container Registry setup
1. Image Registry: <IMAGE_REGISTRY>
#### Creating the Container Registry
az acr create --name <IMAGE_REGISTRY> --resource-group <RESOURCE_GROUP> --sku Basic
#### Enable ACR Admin Access
az acr update -n <IMAGE_REGISTRY> --admin-enabled true

## App Service setup
### Creating the Service Plan (Can be reused)
az appservice plan create --name <RESOURCE_PLAN> --resource-group <RESOURCE_GROUP> --sku B2 --is-linux
### Creating the App Service
az webapp create --resource-group <RESOURCE_GROUP> --plan <RESOURCE_PLAN> --name <APP_NAME> --deployment-container-image-name <IMAGE_NAME>
### Configurations (Restart to take effect)
#### Logging
az webapp log config --name <APP_NAME> --resource-group <RESOURCE_GROUP> --application-logging filesystem --level verbose
#### Updating the Image Name (Name and Version)
az webapp config container set --name <APP_NAME> --resource-group <RESOURCE_GROUP> --docker-custom-image-name <IMAGE_NAME> --docker-registry-server-url <IMAGE_REGISTRY_URL>
### Actions
#### Restarting the webapp
az webapp restart --name <APP_NAME> --resource-group <RESOURCE_GROUP>
#### Tail Logs
az webapp log tail --name <APP_NAME> --resource-group <RESOURCE_GROUP> --verbose

## Build and deploy (cd to project folder with Dockerfile)

### Build Docker Image
#### Frontend only. Build static images
npm run build
#### Login to Registry
az acr login --name <IMAGE_REGISTRY>
#### Building the image in x86_64 (includes tagging)
docker build --no-cache --platform linux/amd64 -t <IMAGE_NAME> .
#### Testing an image locally
docker run -p <PORT>:<PORT> <IMAGE_NAME>

### Tag and Push Docker Image
#### Tagging the image
docker tag <OLD_IMAGE_NAME> <IMAGE_NAME>
#### Inspect the image (in this case, only architecture)
docker inspect <IMAGE_NAME> --format '{{.Architecture}}'
#### Pushing the image
docker push <IMAGE_NAME>
#### Verify image and tags
1. az acr repository list --name <IMAGE_REGISTRY> --output table
2. az acr repository show-tags --name <IMAGE_REGISTRY> --repository <IMAGE_REPO> --output table

### Running the Docker Image
#### Update Image name on App Service
az webapp config container set --name <APP_NAME> --resource-group <RESOURCE_GROUP> --docker-custom-image-name <IMAGE_NAME> --docker-registry-server-url <IMAGE_REGISTRY_URL>
#### Restarting the webapp
az webapp restart --name <APP_NAME> --resource-group <RESOURCE_GROUP>
