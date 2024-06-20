# Application Definition

A FastAPI application that allows simple management of Docker containers through HTTP requests.

## Functionalities

1. Pull Docker container image if not available
2. Run Docker container
3. Start Docker container
4. Stop Docker container
5. Remove Docker container
6. Remove Docker image
7. Search Docker container by name
8. Search Docker image by name
9. List all Docker images
10. List all Docker containers

## Script Demo

1. Basic script that lets you choose options and interact with the API - X
2. Navigation done with character input from the user - X
3. Take user input from CLI if needed (pulling of images, creating containers, etc.) - X
4. Display appropriate messages based on server response (no random JSONs flying around) - X

## Optional

- Create a frontend web application to work with the API
  - Make FastAPI return HTML on requests
  - JavaScript Node.js server to handle frontend
  - ???

## Endpoints

### `/images` - Done

- `/images/pull?{name}` - X
- `/images/remove?{name}` - X
- `/images/list` - X
- `/images/search?{name}` - X

### `/containers` - Done

- `/containers/run?{name}` - X
- `/containers/start?{name}` - X
- `/containers/stop?{name}` - X
- `/containers/remove?{name}` - X
- `/containers/list` - X
- `/containers/search?{name}` - X

---

## Testing Plan

!!!Tests assume the user has `ubuntu:latest` and `ubuntu:22.04` already pulled!!!

### I) Functional Tests

#### `/images/pull?{name}` - Done

1. Pulls existing image - X
2. Says not found when image is not found - X
3. If image tag is not specified, it tries to pull the image with tag `latest` - X

#### `/images/remove?{name}` - Done

1. Removes an existing image - X
2. Says image not found if the image doesn't exist locally - X
3. If image tag is not specified, it tries to remove the image with tag `latest` - X

#### `/images/list` - Not doing because there is no way to guarantee consistency

1. Prints all images
2. Prints an empty list if no images on host

#### `/images/search?{name}` - Done

1. Finds existing image - X
2. Says image doesn't exist if not pulled locally - X
3. If no tag is specified, searches for the image name with tag `latest` - X

#### `/containers/run?{name}` - Done

1. Runs a container with the right image name and tag and container name - X
2. Runs a container with the right image name and container name but no tag (latest) - X
3. Says image not pulled locally if the image doesn't exist - X
4. Returns an assertion error when no container name or image name - X

#### `/containers/start?{name}` - Done

1. Starts an existing container with the correct container name - X
2. Says no such container exists with the name of a non-existing container - X

#### `/containers/stop?{name}` - Done

1. Stops an already started container - X
2. Says no such container if the container doesn't exist - X
3. Says container not running if the container is not running - X

#### `/containers/remove?{name}` - Done

1. Removes an existing container if it is not running - X
2. Says can't remove the container if the container is running - X
3. Says no such container if the container doesn't exist locally - X

#### `/containers/list` - Not doing because there can be no way to guarantee consistency

1. Prints all containers
2. Prints an empty list if no containers

#### `/containers/search?{name}` - Done

1. Finds an existing container by name - X
2. Says container not found when no container with that name - X

