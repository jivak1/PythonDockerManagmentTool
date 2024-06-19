from fastapi import FastAPI, HTTPException

import docker
from docker.models.containers import Container
from docker.errors import ImageNotFound, NotFound

from typing import List

client = docker.from_env()

app = FastAPI()

def check_image_exists(image_name: str, tag: str):
    try:
        manifest = client.images.get_registry_data(f"{image_name}:{tag}")
        return True
    except Exception as e:
        return False
    
def find_image_on_local(image_name: str, tag: str):
    try:
        image = client.images.get(f"{image_name}:{tag}")
        return image
    except ImageNotFound:
        return None
        
def find_container_on_local(container_name: str):
    try:
        container = client.containers.get(container_name)
        return container
    except NotFound:
        return None
def container_is_running(container: Container):
    try:
        return container.status == "running"
    except NotFound:
        return False 

@app.get("/")
def root():
    return {"message": "Hello World! This is a small utility docker application written in python! Have fun :D"}

@app.post("/images/pull")
def pull_image(image_name: str, tag: str | None = "latest"):
    if check_image_exists(image_name, tag):
        client.images.pull(f"{image_name}:{tag}")
        return {"name": f"{image_name}:{tag}"}
    else:
        raise HTTPException(
            status_code=404, detail=f"Image {image_name}:{tag} does not exist on dockerhub"
        )

@app.get("/images/search")
def search_image(image_name: str, tag: str | None = "latest"):
        image = find_image_on_local(image_name, tag)
        
        if image is None:
            raise HTTPException(
            status_code=404, detail=f"Image {image_name}:{tag} is not pulled localy"
            )
        else:
            return {"name": image_name, "tag": tag}
            
@app.delete("/images/remove")
def remove_image(image_name: str, tag: str | None = "latest"):
        image = find_image_on_local(image_name, tag)
      
        if image is None:
            raise HTTPException(
            status_code=404, detail=f"Image {image_name}:{tag} is not pulled localy and can't be removed"
            )
        else:
            client.images.remove(f"{image_name}:{tag}")
            return {"detail": "Image succesfully removed"}

@app.get("/images/list")
def get_images_list() -> List[dict]:
    images = client.images.list()
    images_info = []
    
    for image in images:
        name, tag = image.tags[0].split(":")
        
        images_info.append({
            "name": name,
            "tag": tag,
            "created": image.attrs['Created'],
            "size": image.attrs['Size']
        })
        
    if not images_info:
            raise HTTPException(
            status_code=404, detail=f"No images found locally"
            )
    else:
            return images_info
        
@app.post("/containers/run")
def run_container(image_name: str, container_name: str, tag: str | None = "latest"):    
    image = find_image_on_local(image_name, tag)
        
    if image is None:
        raise HTTPException(
        status_code=404, detail=f"Image {image_name}:{tag} is not pulled localy"
        )
    else:
        client.containers.run(f"{image_name}:{tag}", name=container_name, stdin_open=True, tty=True, detach=True)
    
        return {"image": f"{image_name}:{tag}", "container_name": container_name}
    
@app.patch("/containers/start")
def start_container(container_name: str):
    container = find_container_on_local(container_name)
    
    if container is None:
        raise HTTPException(
        status_code=404, detail=f"Container with name {container_name} not found"
        )
    else:
        container.start()
        return {"container_name": container_name}

@app.patch("/containers/stop")
def stop_container(container_name: str):
    container = find_container_on_local(container_name)

    if container is None:
        raise HTTPException(
        status_code=404, detail=f"Container with name {container_name} not found"
        )
    else:
        container.stop()
        return {"detail": f"Container with name {container_name} exited"}

@app.delete("/containers/remove")
def remove_container(container_name: str):
    container = find_container_on_local(container_name)
    
    if container is None:
      raise HTTPException(
        status_code=404, detail=f"Container with name {container_name} not found"
        )
    else:
        if not container_is_running(container):
            container.remove()
            return {"detail": f"Container {container_name} successfully removed"}
        else:
            raise HTTPException(
                status_code=400, detail=f"Container {container_name} is running. Please stop the container before removing"
            )

@app.get("/containers/search")
def search_container(container_name: str):
    container = find_container_on_local(container_name)
    
    if container is None:
        raise HTTPException(
                status_code=404, detail=f"Container {container_name} not found"
        )
    else:
        return{"detail": f"Container {container_name} found and is {container.status}"}

@app.get("/containers/list")
def list_containers() -> List[dict]:
    containers = client.containers.list(all=True)
    containers_info = []
    
    for container in containers:
        
        
        
        containers_info.append({
            "id": container.short_id,
            "image": container.image.tags[0],
            "name": container.name,
            "status": container.status,
            "created": container.attrs["Created"]
        })
        
    if not containers_info:
            raise HTTPException(
            status_code=404, detail=f"No containers found locally"
            )
    else:
            return containers_info
