from fastapi.testclient import TestClient
from main import app

import docker

app_client = TestClient(app)
docker_client = docker.from_env()

try:
    docker_client.containers.list()
    print("Docker client is working.")
except Exception as e:
        
    print(f"An error occurred: {e}")
    exit()

def is_container_running(container_name):
    container = docker_client.containers.get(container_name)
    return container.status == 'running'

def stop_and_remove_ubuntu_container():
    container = docker_client.containers.get("ubuntu_container")
    
    container.stop()
    
    container.remove()


# def test_pull_image_when_exists():
#     response = app_client.post("http://127.0.0.1:8000/images/pull?image_name=ubuntu&tag=22.04")
    
#     response_json = response.json()
    
    
#     docker_client.images.remove("ubuntu:22.04")
    
#     assert response.status_code == 200
#     assert response_json == {"name": "ubuntu:22.04"}
    
# def test_pull_image_with_no_tag_when_exists():
#     response = app_client.post("http://127.0.0.1:8000/images/pull?image_name=ubuntu")
    
#     response_json = response.json()
    
#     docker_client.images.remove("ubuntu:latest")
    
#     assert response.status_code == 200
#     assert response_json == {"name": "ubuntu:latest"}
    
# def test_pull_image_when_not_exists():
#     response = app_client.post("http://127.0.0.1:8000/images/pull?image_name=noimage&tag=nada")
    
#     response_json = response.json()
        
#     assert response.status_code == 404
#     assert response_json == {"detail": "Image noimage:nada does not exist on dockerhub"}
    
def test_search_image_when_exists():
    # docker_client.images.pull("ubuntu:22.04")
    
    response = app_client.get("http://127.0.0.1:8000/images/search?image_name=ubuntu&tag=22.04")
    
    response_json = response.json()
    
    # docker_client.images.remove("ubuntu:22.04")
    
    assert response.status_code == 200
    assert response_json == {"name": "ubuntu", "tag": "22.04"}
    
def test_search_image_with_no_tag_when_exists():
    # docker_client.images.pull("ubuntu:latest")
    
    response = app_client.get("http://127.0.0.1:8000/images/search?image_name=ubuntu")
    
    response_json = response.json()
    
    # docker_client.images.remove("ubuntu:latest")
    
    assert response.status_code == 200
    assert response_json == {"name": "ubuntu", "tag": "latest"}
    
def test_search_image_when_not_exists():
    response = app_client.get("http://127.0.0.1:8000/images/search?image_name=noimage&tag=nada")
    
    response_json = response.json()
        
    assert response.status_code == 404
    assert response_json == {"detail": "Image noimage:nada is not pulled localy"}

# def test_remove_image_when_exists():
#     docker_client.images.pull("ubuntu:22.04")
    
#     response = app_client.delete("http://127.0.0.1:8000/images/remove?image_name=ubuntu&tag=22.04")
    
#     response_json = response.json()
    
#     assert response.status_code == 200
#     assert response_json == {"detail": "Image succesfully removed"}
    
# def test_remove_image_with_no_tag_when_exists():
#     docker_client.images.pull("ubuntu:latest")
    
#     response = app_client.delete("http://127.0.0.1:8000/images/remove?image_name=ubuntu")
    
#     response_json = response.json()
    
#     assert response.status_code == 200
#     assert response_json == {"detail": "Image succesfully removed"}
    
# def test_remove_image_when_not_exists():    
#     response = app_client.delete("http://127.0.0.1:8000/images/remove?image_name=noimage&tag=nada")
    
#     response_json = response.json()
    
#     assert response.status_code == 404
#     assert response_json == {"detail": "Image noimage:nada is not pulled localy and can't be removed"}
    
def test_run_container_when_image_exists():
    # docker_client.images.pull("ubuntu:22.04")
    
    response = app_client.post("http://127.0.0.1:8000/containers/run?image_name=ubuntu&container_name=ubuntu_container&tag=22.04")
    
    stop_and_remove_ubuntu_container()
    
    # docker_client.images.remove("ubuntu:22.04")

    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json == {"image": "ubuntu:22.04", "container_name": "ubuntu_container"}
    
def test_run_container_when_image_with_no_tag_exists():
    # docker_client.images.pull("ubuntu:latest")
    
    response = app_client.post("http://127.0.0.1:8000/containers/run?image_name=ubuntu&container_name=ubuntu_container")
    
    stop_and_remove_ubuntu_container()

    # docker_client.images.remove("ubuntu:latest")

    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json == {"image": "ubuntu:latest", "container_name": "ubuntu_container"}
    
def test_run_container_when_image_not_pulled():
    response = app_client.post("http://127.0.0.1:8000/containers/run?image_name=noimage&container_name=ubuntu_container&tag=nada")
    
    response_json = response.json()
    
    assert response.status_code == 404
    assert response_json == {"detail": "Image noimage:nada is not pulled localy"}
    
def test_run_container_fails_without_arguments():
    response = app_client.post("http://127.0.0.1:8000/containers/run")
        
    assert response.status_code == 422
    
def test_start_container_that_exists():
    # docker_client.images.pull("ubuntu")
    
    docker_client.containers.run("ubuntu", name="ubuntu_container", detach=True)
    
    response = app_client.patch("http://127.0.0.1:8000/containers/start?container_name=ubuntu_container")
    
    stop_and_remove_ubuntu_container()
    
    # docker_client.images.remove("ubuntu")
    
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json == {"container_name": "ubuntu_container"}
    
def test_start_container_that_not_exists():
    response = app_client.patch("http://127.0.0.1:8000/containers/start?container_name=nocontainer_exists")
    
    response_json = response.json()

    assert response.status_code == 404
    assert response_json == {"detail": "Container with name nocontainer_exists not found"}
    
def test_stops_container_that_exists():
    # docker_client.images.pull("ubuntu")
    
    docker_client.containers.run("ubuntu", name="ubuntu_container", stdin_open=True, tty=True, detach=True)
    
    docker_client.containers.get("ubuntu_container").start()
    
    response = app_client.patch("http://127.0.0.1:8000/containers/stop?container_name=ubuntu_container")

    stop_and_remove_ubuntu_container()
    
    # docker_client.images.remove("ubuntu")
    
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json == {"detail": "Container with name ubuntu_container exited"}

def test_stops_container_that_exists():
    # docker_client.images.pull("ubuntu")
    
    docker_client.containers.run("ubuntu", name="ubuntu_container", stdin_open=True, tty=True, detach=True)
        
    response = app_client.patch("http://127.0.0.1:8000/containers/stop?container_name=ubuntu_container")

    container = docker_client.containers.get("ubuntu_container")
    
    container.remove()
    
    # docker_client.images.remove("ubuntu")
    
    response_json = response.json()
    
    assert response.status_code == 409
    assert response_json == {"detail": "Container with name ubuntu_container not running"}
    
def test_stop_container_that_not_exists():
    response = app_client.patch("http://127.0.0.1:8000/containers/stop?container_name=nocontainer_exists")
    
    response_json = response.json()

    assert response.status_code == 404
    assert response_json == {"detail": "Container with name nocontainer_exists not found"}

def test_remove_container_that_exists_and_is_stopped():
    # docker_client.images.pull("ubuntu")
    
    docker_client.containers.run("ubuntu", name="ubuntu_container", stdin_open=True, tty=True, detach=True)
    
    container = docker_client.containers.get("ubuntu_container")
    
    container.stop()
    
    response = app_client.delete("http://127.0.0.1:8000/containers/remove?container_name=ubuntu_container")

    
    # docker_client.images.remove("ubuntu")
    
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json == {"detail": "Container ubuntu_container successfully removed"}
    
def test_remove_container_that_exists_and_is_running():
    # docker_client.images.pull("ubuntu")
    
    docker_client.containers.run("ubuntu", name="ubuntu_container", stdin_open=True, tty=True, detach=True)        
    
    response = app_client.delete("http://127.0.0.1:8000/containers/remove?container_name=ubuntu_container")

    stop_and_remove_ubuntu_container()
    
    # docker_client.images.remove("ubuntu")
    
    response_json = response.json()
    
    assert response.status_code == 400
    assert response_json == {"detail": "Container ubuntu_container is running. Please stop the container before removing"}
    
def test_remove_container_that_not_exists():
    response = app_client.delete("http://127.0.0.1:8000/containers/remove?container_name=nocontainer_nada")
        
    response_json = response.json()
    
    assert response.status_code == 404
    assert response_json == {"detail": "Container with name nocontainer_nada not found"}

def test_find_container_that_exists_and_is_running():
    # docker_client.images.pull("ubuntu")
    
    docker_client.containers.run("ubuntu", name="ubuntu_container", stdin_open=True, tty=True, detach=True)
    
    container = docker_client.containers.get("ubuntu_container")
    
    container.start()
    
    response = app_client.get("http://127.0.0.1:8000/containers/search?container_name=ubuntu_container")
    
    stop_and_remove_ubuntu_container()
    
    # docker_client.images.remove("ubuntu")
  
    response_json = response.json()
    
    assert response.status_code == 200
    assert response_json == {"detail": "Container ubuntu_container found and is running"}
     
def test_find_container_that_exists_and_is_exited():
    # docker_client.images.pull("ubuntu")

    docker_client.containers.run("ubuntu", name="ubuntu_container", stdin_open=True, tty=True, detach=True)
    
    docker_client.containers.get("ubuntu_container").stop()

    response = app_client.get("http://127.0.0.1:8000/containers/search?container_name=ubuntu_container")
    
    response_json = response.json()
    
    stop_and_remove_ubuntu_container()
    
    # docker_client.images.remove("ubuntu")
    
    assert response.status_code == 200
    assert response_json == {"detail": "Container ubuntu_container found and is exited"}
    
def test_find_container_that_not_exists():
    response = app_client.get("http://127.0.0.1:8000/containers/search?container_name=nocontainer_nada")
    
    response_json = response.json()
    
    assert response.status_code == 404
    assert response_json == {"detail": "Container nocontainer_nada not found"}
