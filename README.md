# FastAPI Docker Manager

## Overview

The FastAPI Docker Manager is a web application that provides an HTTP API for managing Docker containers and images. It allows users to perform various operations such as pulling images, running containers, and more through simple HTTP requests.

## Functionalities

1. Pull Docker container image if not available (Done)
2. Run Docker container (Done)
3. Start Docker container (Done)
4. Stop Docker container (Done)
5. Remove Docker container (Done)
6. Remove Docker image (Done)
7. Search Docker container by name (Done)
8. Search Docker image by name (Done)
9. List all Docker images (Done)
10. List all Docker containers (Done)

## Script Demo

1. Basic script that lets you choose options and interact with the API (Done)
2. Navigation done with character input from the user (Done)
3. Take user input from CLI if needed (pulling images, creating containers, etc.) (Done)
4. Display appropriate messages based on server response (no random JSONs flying around) (Done)

## Optional Features

- Create a frontend web application to work with the API
  - Make FastAPI return HTML on requests (Pending)
  - JavaScript Node.js server to handle frontend (Pending)
  - Additional features to be determined (Pending)

## API Endpoints

### Image Management

- `POST /images/pull?name={name}&tag={tag}` - Pull an image (Done)
- `DELETE /images/remove?name={name}&tag={tag}` - Remove an image (Done)
- `GET /images/list` - List all images (Done)
- `GET /images/search?name={name}&tag={tag}` - Search for an image (Done)

### Container Management

- `POST /containers/run?name={name}&image_name={image_name}&tag={tag}` - Run a container (Done)
- `PATCH /containers/start?name={name}` - Start a container (Done)
- `PATCH /containers/stop?name={name}` - Stop a container (Done)
- `DELETE /containers/remove?name={name}` - Remove a container (Done)
- `GET /containers/list` - List all containers (Done)
- `GET /containers/search?name={name}` - Search for a container (Done)

## Testing Plan

!!!Tests assume the user has `ubuntu:latest` and `ubuntu:22.04` already pulled!!!

### Functional Tests

#### Image Operations

- `POST /images/pull?name={name}&tag={tag}` - Test pulling existing and non-existing images, and default to `latest` tag if not specified. (Done)
- `DELETE /images/remove?name={name}&tag={tag}` - Test removing existing and non-existing images, and default to `latest` tag if not specified. (Done)
- `GET /images/search?name={name}&tag={tag}` - Test searching for existing and non-existing images, and default to `latest` tag if not specified. (Done)

#### Container Operations

- `POST /containers/run?name={name}&image_name={image_name}&tag={tag}` - Test running containers with correct and incorrect image names/tags. (Done)
- `PATCH /containers/start?name={name}` - Test starting existing and non-existing containers. (Done)
- `PATCH /containers/stop?name={name}` - Test stopping running and non-running containers. (Done)
- `DELETE /containers/remove?name={name}` - Test removing existing, running, and non-existing containers. (Done)
- `GET /containers/search?name={name}` - Test searching for existing and non-existing containers. (Done)

Note: Some tests related to listing images and containers are not included due to the inability to guarantee consistency in the test environment.

## Application deployment:

### Docker containerisation

- Created a dockerfile, to containerise the application
- Container runs, but needs docker.sock to be mounted as volume

### Kubernetes Deployment

- Created a kubernetes deployment file, that creates pods with 3 instances of the app
- Created a NodePort service to expose the application to localhost and route trafic to any of the pods

Note: The built image shuld be archived in a .tar file and coppied to the kubernetes namespace, so that it can be pulled by the deployment

