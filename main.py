import os
import json
from typing import Dict, Any, List, Tuple

from fastapi import FastAPI, Request, Response
from loguru import logger as log
import dotenv
import docker.models.containers

dotenv.load_dotenv()

app = FastAPI()
docker_client = docker.from_env()
DEPLOY_TOKEN = os.getenv("DEPLOY_TOKEN")
if DEPLOY_TOKEN is None:
    log.error("DEPLOY_TOKEN isn`t set! Server stopped.")
    exit(-1)


def is_authenticated(request: Request):
    if request.headers.get("Authorization") != DEPLOY_TOKEN:
        return False
    return True


def deploy_container(image_name: str, container_name: str,
                     ports: dict = None, environment: dict = None) -> Tuple[Dict[str, Any], int]:
    try:
        log.info(f"Pull image {image_name}, name = {container_name}")
        docker_client.images.pull(image_name)
        log.info("PULL SUCCESS")

        log.info(f"Kill old container {container_name}")
        kill_container(container_name)
        log.info("KILL SUCCESS")

        log.info("Start container")
        docker_client.containers.run(
            image=image_name,
            name=container_name,
            detach=True,
            ports=ports,
            restart_policy={
                "name": "always"
            },
            environment=environment
        )
        log.info("START SUCCESS")

    except Exception as e:
        log.error(f"Error while deploy container {container_name},\n{e}")
        return {"status": False, "error": str(e)}, 400

    log.info("DEPLOY SUCCESS")
    log.info(f"Container {container_name} deployed")
    return {"status": True}, 200


def kill_container(container_name: str):
    try:
        container = docker_client.containers.get(container_name)
        container.kill()
        log.info(f"Container {container_name} killed")

    except Exception as e:
        log.warning(f"Error while killing container {container_name},\n{e}")

    finally:
        log.info(docker_client.containers.prune())


def get_container_name(request_json: Dict[str, Any]) -> Tuple[str, str]:
    owner = request_json.get("owner")
    repository = request_json.get("repository")
    tag = request_json.get("tag", "latest").replace('v', '')
    if owner and repository and tag:
        return f"{owner}/{repository}:{tag}", repository
    if repository and tag:
        return f"{repository}:{tag}", repository


def get_container_data(container: docker.models.containers.Container) -> Dict[str, Any]:
    return {
        "short_id": container.short_id,
        "name": container.name,
        "tags": container.image.tags,
        "created": container.attrs["Created"],
        "status": container.status,
        "ports": container.ports
    }


def get_active_containers() -> List[Dict[str, Any]]:
    containers = []
    for container in docker_client.containers.list():
        containers.append(get_container_data(container))
    return containers


@app.get("/")
@app.post("/")
async def root(request: Request):
    if not is_authenticated(request):
        return Response(json.dumps({"message": "Authentication failed!"}), 401)

    response_data = None
    status_code = None

    if request.method == "GET":
        response_data, status_code = get_active_containers(), 200

    elif request.method == "POST":
        request_json = await request.json()
        log.info(f"Received data: {request_json}")
        image_name, container_name = get_container_name(request_json)
        ports = request_json.get("ports")
        environment = request_json.get("environment")
        log.info(f"Try deploy new container {image_name}, {container_name}")
        response_data, status_code = deploy_container(image_name, container_name, ports, environment)

    return Response(json.dumps(response_data), status_code)
