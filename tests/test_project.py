import pytest

from main import mcp
from utils import (
    validate_models, 
    ensure_request_fails, 
    ensure_request_raises_validation_error,
    ensure_request_raises_validation_error_when_omitting_an_arg,
    create_timestamp,
)
from models import (
    CreateProjectRequest,
    ProjectListResponse,
    RestResponse,
)


# Static helpers for common operations:
class Project:

    @staticmethod
    async def create(name=f"Project {create_timestamp()}", language='Py'):
        output_model = await validate_models(
            mcp, 'create_project', {'name': name, 'language': language},
            ProjectListResponse
        )
        return output_model.projects[0]

    @staticmethod
    async def read(**kwargs):
        output_model = await validate_models(
            mcp, 'read_project', kwargs, ProjectListResponse
        )
        return output_model.projects

    @staticmethod
    async def update(id_, **kwargs):
        await validate_models(
            mcp, 'update_project', {'projectId': id_} | kwargs, RestResponse
        )

    @staticmethod
    async def delete(id_):
        await validate_models(
            mcp, 'delete_project', {'projectId': id_}, RestResponse
        )

    @staticmethod
    async def list():
        output_model = await validate_models(
            mcp, 'list_projects', output_class=ProjectListResponse
        )
        return output_model.projects


# Test suite:
class TestProject:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_project(self, language):
        name = f"Project {create_timestamp()}"
        project = await Project.create(name, language)
        # Test if the name and language are correct.
        assert project.name == name
        assert project.language.value == language
        # Delete the project to clean up.
        await Project.delete(project.projectId)

    @pytest.mark.asyncio
    async def test_create_project_with_invalid_args(self):
        tool_name = 'create_project'
        request_class = CreateProjectRequest
        minimal_payload = {'name': 'Test Project', 'language': 'Py'}
        # Try to create a project without providing all the arguments.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, request_class, minimal_payload
        )
        # Try to create a project with an unsupported language.
        await ensure_request_raises_validation_error(
            tool_name, request_class, minimal_payload | {'language': 'C++'}
        )

    @pytest.mark.asyncio
    async def test_read_project(self):
        # Create a project.
        name = f"Project {create_timestamp()}"
        language = 'Py'
        id_ = (await Project.create(name, language)).projectId
        # Read the project.
        project = (await Project.read(projectId=id_))[0]
        # Test if the name and language are correct.
        assert project.name == name
        assert project.language.value == language
        # Delete the project to clean up.
        await Project.delete(id_)
        # Test if we can read multiple projects.
        num_projects = 2
        ids = [
            (await Project.create(name, language)).projectId
            for i in range(num_projects)
        ]
        projects = await Project.read(end=num_projects)
        assert len(projects) == num_projects
        # Delete the projects to clean up.
        for id_ in ids:
            await Project.delete(id_)

    @pytest.mark.asyncio
    async def test_read_project_with_invalid_args(self):
        payloads = [
            # Try to read a project that doesn't exist.
            {'projectId': -1},
            # Try to read a list of projects where start >= end.
            {'start': 1, 'end': 1},
            {'start': 1, 'end': 0}
        ]
        for payload in payloads:
            await ensure_request_fails(mcp, 'read_project', payload)
        

    @pytest.mark.asyncio
    async def test_update_project(self):
        # Create a project.
        id_ = (await Project.create()).projectId
        
        # Update the project name.
        new_name = f"Project {create_timestamp()}"
        await Project.update(id_, name=new_name)
        # Test if the new name is correct.
        project = (await Project.read(projectId=id_))[0]
        assert project.name == new_name
        
        # Update the project description.
        new_description = f"Description {create_timestamp()}"
        await Project.update(id_, description=new_description)
        # Test if the new description is correct.
        project = (await Project.read(projectId=id_))[0]
        assert project.description == new_description
        
        # Update the project name and description.
        new_name = f"Project {create_timestamp()}"
        new_description = f"Description {create_timestamp()}"
        await Project.update(
            id_, name=new_name, description=new_description
        )
        # Test if the new name & description are correct.
        project = (await Project.read(projectId=id_))[0]
        assert project.name == new_name
        assert project.description == new_description

        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    async def test_update_project_with_a_nonunique_name(self):
        # Create 2 projects.
        name_1 = f"Project {create_timestamp()}"
        id_1 = (await Project.create(name_1)).projectId
        name_2 = f"Project {create_timestamp()}"
        id_2 = (await Project.create(name_2)).projectId
        # Try updating the project names to match.
        await ensure_request_fails(
            mcp, 'update_project', {'projectId': id_2, 'name': name_1}
        )
        # Delete the projects.
        await Project.delete(id_1)
        await Project.delete(id_2)

    @pytest.mark.asyncio
    async def test_delete_projects_with_invalid_args(self):
        # Try to delete a project that doesn't exist.
        await ensure_request_fails(mcp, 'delete_project', {'projectId': -1})

    @pytest.mark.asyncio
    async def test_list_projects(self):
        await Project.list()
