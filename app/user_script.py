import requests

from typing import List

import math

# pull image
# print(requests.get("http://127.0.0.1:8000/images/pull?image_name=ubuntu&tag=22.04").json())

# find image
# print(requests.get("http://127.0.0.1:8000/images/search?image_name=ubuntu&tag=22.04").json())

#remove image
# print(requests.delete("http://127.0.0.1:8000/images/remove?image_name=ubuntu&tag=22.04").json())

#list images
# print(requests.get("http://127.0.0.1:8000/images/list").json())


# Run container
# print(requests.post("http://127.0.0.1:8000/containers/run?image_name=ubuntu&container_name=ubuntu_container").json())

# Start container
# print(requests.patch("http://127.0.0.1:8000/containers/start?container_name=ubuntu_container").json())

# Stop container
# print(requests.patch("http://127.0.0.1:8000/containers/stop?container_name=ubuntu_container").json())

#Remove container
# print(requests.delete("http://127.0.0.1:8000/containers/remove?container_name=ubuntu_container").json())

#Find container
# print(requests.get("http://127.0.0.1:8000/containers/search?container_name=ubuntu_container").json())

#List containers
# print(requests.get("http://127.0.0.1:8000/containers/list").json())

def go_forward() -> bool:
    user_input = input("Would ou like to continue...[y/n]")
    if user_input == "y" or user_input == "Y":
        return True
    else:
        return False

def get_image_info() -> List[str]:
    image_info = input("Please input name of image: ")
            
    image_info_split = image_info.split(":")
    
    return image_info_split

def get_container_name() -> str:
    container_name = input("Please input container name:")
    
    return container_name

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def print_image_list(response_json):
    print(f"{'Image Name':<20}{'Tag':<15}{'Created':<35}{'Size':<10}")
    print(f"{'-'*20}{'-'*15}{'-'*35}{'-'*10}")
            
    for info in response_json:               
        print(f"{info['name']:<20}{info['tag']:<15}{info['created']:<35}{convert_size(info['size']):<10}")
        
def print_container_list(response_json):
    print(f"{'Container ID':<20}{'Image':<30}{'Name':<25}{'Status':<15}{'Created':<35}")
    print(f"{'-'*20}{'-'*30}{'-'*25}{'-'*15}{'-'*35}")
    
    for container in response_json:
        print(f"{container['id']:<20}{container['image']:<30}{container['name']:<25}{container['status']:<15}{container['created']:<35}")

while True:
    print("Please select an option: \n" 
        + "1) Pull an image from dockerhub\n" 
        + "2)Find local image\n"
        + "3)Remove image localy\n" 
        + "4)List all available images\n" 
        + "5)Run a container from image\n" 
        + "6)Start container\n" 
        + "7)Stop a running container\n" 
        + "8)Remove a container(must be stopped first)\n"
        + "9)Find container by name\n" 
        + "10)List all containers\n"
        + "11)Exit the application")

    option = input("Waiting for selection: ")

    match option:
        case "1":
            image_info_split = get_image_info()
               
            response = requests.post(f"http://127.0.0.1:8000/images/pull?image_name={image_info_split[0]}" + (f"&tag={image_info_split[1]}" if len(image_info_split) == 2 else ""))

            response_json = response.json()
            
            if response.status_code == 200:
                print(f"Image {response_json['name']} pulled successfuly")
            else:
                print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
            
        case "2":                    
            image_info_split = get_image_info()
            
            response = requests.get(f"http://127.0.0.1:8000/images/search?image_name={image_info_split[0]}" + (f"&tag={image_info_split[1]}" if len(image_info_split) == 2 else ""))
            
            response_json = response.json()
            
            if response.status_code == 200:
                print(f"Image {response_json['name']}:{response_json['tag']} found locally")
            else:
                print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
            
        case "3":
            image_info_split = get_image_info()
            
            response = requests.delete(f"http://127.0.0.1:8000/images/remove?image_name={image_info_split[0]}" + (f"&tag={image_info_split[1]}" if len(image_info_split) == 2 else ""))
            
            response_json = response.json()
                        
            print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
        case "4":            
            response = requests.get(f"http://127.0.0.1:8000/images/list")
            
            response_json = response.json()
            
            print_image_list(response_json)
            
            if(go_forward()):
                continue
            else:
                break
        case "5":
            image_info_split = get_image_info()
            
            container_name = get_container_name()
            
            response = requests.post(f"http://127.0.0.1:8000/containers/run?image_name={image_info_split[0]}" + (f"&tag={image_info_split[1]}" if len(image_info_split) == 2 else "") + f"&container_name={container_name}")

            response_json = response.json()
            
            if response.status_code == 200:
                print(f"Container {response_json['container_name']} was successfully ran from image {response_json['image']}")
            else:
                print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
        case "6":
            container_name = get_container_name()
            
            response = requests.patch(f"http://127.0.0.1:8000/containers/start?container_name={container_name}")
            
            response_json = response.json()
            
            if response.status_code == 200:
                print(f"Container {response_json['container_name']} started successfully")
            else:
                print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
        case "7":
            container_name = get_container_name()
            
            response = requests.patch(f"http://127.0.0.1:8000/containers/stop?container_name={container_name}")
            
            response_json = response.json()
            
            print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
        case "8":
            container_name = get_container_name()
            
            response = requests.delete(f"http://127.0.0.1:8000/containers/remove?container_name={container_name}")
            
            response_json = response.json()
            
            print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
        case "9":
            container_name = get_container_name()
            
            response = requests.get(f"http://127.0.0.1:8000/containers/search?container_name={container_name}")
            
            response_json = response.json()
            
            print(response_json["detail"])
            
            if(go_forward()):
                continue
            else:
                break
        case "10":
            response = requests.get(f"http://127.0.0.1:8000/containers/list")
            
            response_json = response.json()
            
            print_container_list(response_json)
            
            if(go_forward()):
                continue
            else:
                break
        case "11":
            break
        case _:
            continue
        

