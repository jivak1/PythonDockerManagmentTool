from fastapi.testclient import TestClient
from main import app

import docker

app_client = TestClient(app)
docker_client = docker.from_env()

def is_container_running(container_name):
    container = docker_client.containers.get(container_name)
    return container.status == 'running'


def test_pull_image_when_exists():
    response = app_client.post("http://127.0.0.1:8000/images/pull?image_name=ubuntu&tag=22.04")
    
    response_json = response.json()
    
    
    docker_client.images.remove("ubuntu:22.04")
    
    assert response.status_code == 200
    assert response_json == {"name": "ubuntu:22.04"}
    
def test_pull_image_with_no_tag_when_exists():
    response = app_client.post("http://127.0.0.1:8000/images/pull?image_name=ubuntu")
    
    response_json = response.json()
    
    docker_client.images.remove("ubuntu:latest")
    
    assert response.status_code == 200
    assert response_json == {"name": "ubuntu:latest"}
    
def test_pull_image_when_not_exists():
    response = app_client.post("http://127.0.0.1:8000/images/pull?image_name=noimage&tag=nada")
    
    response_json = response.json()
        
    assert response.status_code == 404
    assert response_json == {"detail": "Image noimage:nada does not exist on dockerhub"}
    
def test_search_image_when_exists():
    docker_client.images.pull("ubuntu:22.04")
    
    response = app_client.get("http://127.0.0.1:8000/images/search?image_name=ubuntu&tag=22.04")
    
    response_json = response.json()
    
    docker_client.images.remove("ubuntu:22.04")
    
    assert response.status_code == 200
    assert response_json == {"name": "ubuntu:22.04"}
    
def test_search_image_with_no_tag_when_exists():
    docker_client.images.pull("ubuntu:latest")
    
    response = app_client.get("http://127.0.0.1:8000/images/search?image_name=ubuntu")
    
    response_json = response.json()
    
    docker_client.images.remove("ubuntu:latest")
    
    assert response.status_code == 200
    assert response_json == {"name": "ubuntu:latest"}
    
def test_search_image_when_not_exists():
    response = app_client.get("http://127.0.0.1:8000/images/search?image_name=noimage&tag=nada")
    
    response_json = response.json()
        
    assert response.status_code == 404
    assert response_json == {"detail": "Image noimage:nada is not pulled localy"}


