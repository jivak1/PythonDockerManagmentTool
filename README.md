Application definition

A FastAPI application, that allowes simple managment of docker containers trough HTTP requests

Functionalities:
1-Pull docker container image if not available
2-Run docker container
3-Start docker container
4-Stop docker container
5-Remove docker container
6-Remove docker image
7-Search docker container by name
8-Search docker image by name
9-List all docker images
10-List all docker containers

Script demo:
1-Basic script that lets you choose options and interact with the api - X
2-Navigation done with character input from the user - X
3-Take user input from cli if needed(pulling of images etc, creating containers and etc) - X
4-Display appropreate messages based on server response(no random jsons flying around) - X

Optional:
-Create frontend web application to work with the api
a)Make FastAPI return HTML on requests
b)JavaScript node.js server to handle frontend
c)???
----------------------------------------------------------------------
Endpoints

/
---------------------------
/image - Done

/images/pull?{name} - X

/images/remove?{name} - X

/images/list - X

/images/search?{name} - X
---------------------------
/containers - Done

/containers/run?{name} - X

/containers/start?{name} - X

/containers/stop?{name} - X

/containers/remove?{name} - X

/containers/list - X

containers/search?{name} - X
----------------------------



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
!!!Test assume the user has ubuntu:latest and ubuntu:22.04 already pulled!!!
Testing plan: 

I)Functional tests:
###########################################
/images/pull?{name} - Done
1)Pulls existing image - X
2)Says not found when image is not found - X
3)If image tag is not specified it tries to pull image with tag latest - X
-------------------------------------------
/images/remove?{name} - Done
1)Removes an existing image - X
2)Says image not found if image doesnt exist on local - X
3)If image tag is not specifiedit tryes to remove image with tag latest - X
-------------------------------------------
/images/list - Not doing bcs there is no way to guarantee consistency
1)Prints all images
2)Prints empty list if no images on host
-------------------------------------------
/images/search?{name} - Done
1)Finds existing image - X
2)Says image doesnt exist if not pulled to local - X
3)If no tag is specified searches for image name with tag "latest" - X
------------------------------------------
/containers/run?{name} - Done
1)Runs container with the right image name and tag and container name - X
2)Runs container with the right image name and container name but no tag(latest) - X
3)Says image not pulled localy if image doesnt exist - X
4)Returns asertation error when no container name or image name - X
-------------------------------------------
/containers/start?{name} - Done
1)Starts existing container with the correct container name - X
2)Says No such container exists with name of unexisting container - X
-------------------------------------------
/containers/stop?{name} - Done
1)Stops already started container - X
2)Says no such container if container doesnt exist - X
3)Says container not running if container not running - X
-------------------------------------------
/containers/remove?{name} - Done
1)Removes existing container if it is not running - X
2)Says cant remove container if container running - X
3)Says no such container if container doesnt exist on local - X
-------------------------------------------
/containers/list - Not doing bcs there can be no way to guarantee consistency
1)Prints all containrs
2)Prints empty list if no containers
-------------------------------------------
containers/search?{name} - Done
1)Finds existing container by name - X
2)Says container not found when no container with that name - X
------------------------------------------
