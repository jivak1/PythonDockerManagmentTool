# Application Definition

A FastAPI application that allows simple management of docker containers through HTTP requests.

## Functionalities

1. Pull docker container image if not available
2. Run docker container
3. Start docker container
4. Stop docker container
5. Remove docker container
6. Remove docker image
7. Search docker container by name
8. Search docker image by name
9. List all docker images
10. List all docker containers

## Script Demo

1. Basic script that lets you choose options and interact with the API - X
2. Navigation done with character input from the user - X
3. Take user input from CLI if needed (pulling of images, creating containers, etc.) - X
4. Display appropriate messages based on server response (no random JSONs flying around) - X

## Optional

- Create frontend web application to work with the API
  - Make FastAPI return HTML on requests
  - JavaScript node.js server to handle frontend
  - ???

## Endpoints

### `/`

### `/image` - Done

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

!!!Test assume the user has `ubuntu:latest` and `ubuntu:22.04` already pulled!!!

### I) Functional Tests

#### `/images/pull?{name}` - Done

1. Pulls existing image - X
2. Says not found when image is not found - X
3. If image tag is not specified, it tries to pull image with tag `latest` - X

#### `/images/remove?{name}` - Done

1. Removes an existing image - X
2. Says image not found if image doesn't exist locally - X
3. If image tag is not specified, it tries to remove image with tag `latest` - X

#### `/images/list` - Not doing because there is no way to guarantee consistency

1. Prints all images
2. Prints empty list if no images on host

#### `/images/search?{name}` - Done

1. Finds existing image - X
2. Says image doesn't exist if not pulled locally - X
3. If no tag is specified, searches for image name with tag `latest` - X

#### `/containers/run?{name}` - Done

1. Runs container with the right image name and tag and container name - X
2. Runs container with the right image name and container name but no tag (latest) - X
3. Says image not pulled locally if image doesn't exist - X
4. Returns assertion error when no container name or image name - X

#### `/containers/start?{name}` - Done

1. Starts existing container with the correct container name - X
2. Says no such container exists with the name of a non-existing container - X

#### `/containers/stop?{name}` - Done

1. Stops already started container - X
2. Says no such container if container doesn't exist - X
3. Says container not running if container not running - X

#### `/containers/remove?{name}` - Done

1. Removes existing container if it is not running - X
2. Says can't remove container if container running - X
3. Says no such container if container doesn't exist locally - X

#### `/containers/list` - Not doing because there can be no way to guarantee consistency

1. Prints all containers
2. Prints empty list if no containers

#### `/containers/search?{name}` - Done

1. Finds existing container by name - X
2. Says container not found when no container with that name - X
