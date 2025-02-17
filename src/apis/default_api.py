# coding: utf-8

from typing import Dict, List, Any  # noqa: F401

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

import controller.tasks
from controller import info, tasks
from models.extra_models import TokenModel  # noqa: F401
from models.response import Response
from models.service_info import ServiceInfo
from models.task import Task
from models.tasks_put_request import TasksPutRequest
from models.tasks_task_id_data_put200_response import TasksTaskIdDataPut200Response
from models.tasks_task_id_patch_request import TasksTaskIdPatchRequest


router = APIRouter()

@router.get(
    "/info",
    responses={
        200: {"model": ServiceInfo, "description": "OK"},
    },
    tags=["default"],
    summary="return conding service identification",
    response_model_by_alias=True,
)
async def info_get(
) -> ServiceInfo:
    return info.get_info()


@router.get(
    "/tasks",
    responses={
        200: {"model": List[Task], "description": "OK"},
    },
    tags=["default"],
    summary="get list of all tasks",
    response_model_by_alias=True,
)
async def tasks_get(
) -> List[Task]:
    return tasks.list_tasks()


@router.put(
    "/tasks",
    responses={
        200: {"model": Task, "description": "OK"},
    },
    tags=["default"],
    summary="add a task",
    response_model_by_alias=True,
)
async def tasks_put(
    tasks_put_request: TasksPutRequest = Body(None, description=""),
) -> Task:
    return tasks.create(tasks_put_request)


@router.delete(
    "/tasks/{task_id}/data/{chunk_id}",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="delete a chunk of data from a specific task",
    response_model_by_alias=True,
)
async def tasks_task_id_data_chunk_id_delete(
    task_id: str = Path(..., description=""),
    chunk_id: str = Path(..., description=""),
) -> None:
    return controller.tasks.delete_data(task_id, chunk_id)


@router.get(
    "/tasks/{task_id}/data/{chunk_id}",
    responses={
        200: {"model": List[Response], "description": "OK"},
    },
    tags=["default"],
    summary="retrieve a chunk of data from a specific task",
    response_model_by_alias=True,
)
async def tasks_task_id_data_chunk_id_get(
    task_id: str = Path(..., description=""),
    chunk_id: str = Path(..., description=""),
):
    return controller.tasks.get_data(task_id, chunk_id)


@router.put(
    "/tasks/{task_id}/data",
    responses={
        200: {"model": TasksTaskIdDataPut200Response, "description": "OK"},
    },
    tags=["default"],
    summary="add a chunk of data for a specific task",
    response_model_by_alias=True,
)
async def tasks_task_id_data_put(
    task_id: str = Path(..., description=""),
    response: List[Response] = Body(None, description=""),
) -> TasksTaskIdDataPut200Response:
    return tasks.add_data(task_id, response)


@router.delete(
    "/tasks/{task_id}",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    response_model_by_alias=True,
)
async def tasks_task_id_delete(
    task_id: str = Path(..., description=""),
) -> None:
    return tasks.delete(task_id)


@router.get(
    "/tasks/{task_id}",
    responses={
        200: {"model": Task, "description": "OK"},
    },
    tags=["default"],
    summary="get specific task",
    response_model_by_alias=True,
)
async def tasks_task_id_get(
    task_id: str = Path(..., description=""),
) -> Task:
    return tasks.get(task_id)


@router.patch(
    "/tasks/{task_id}/instructions",
    responses={
        200: {"description": "OK"},
    },
    tags=["default"],
    summary="update instructions",
    response_model_by_alias=True,
)
async def tasks_task_id_instructions_patch(
    task_id: str = Path(..., description=""),
    instructions: Dict[str, Any] = Body(None, description=""),
) -> None:
    return tasks.update_instructions(task_id, instructions)


@router.patch(
    "/tasks/{task_id}",
    responses={
        200: {"model": Task, "description": "OK"},
    },
    tags=["default"],
    summary="perform action on task",
    response_model_by_alias=True,
)
async def tasks_task_id_patch(
    task_id: str = Path(..., description=""),
    tasks_task_id_patch_request: TasksTaskIdPatchRequest = Body(None, description=""),
) -> Task:
    return tasks.action(task_id, tasks_task_id_patch_request.action)
