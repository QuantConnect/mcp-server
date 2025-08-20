import pytest
from time import sleep

from main import mcp
from test_project import Project
from utils import (
    validate_models, 
    ensure_request_fails, 
    ensure_request_raises_validation_error,
    ensure_request_raises_validation_error_when_omitting_an_arg
)
from models import (
    CreateCompileRequest, 
    ReadCompileRequest, 
    CreateCompileResponse,
    ReadCompileResponse
)


# Static helpers for common operations:
class Compile:

    @staticmethod
    async def create(project_id):
        output_model = await validate_models(
            mcp, 'create_compile', {'projectId': project_id},
            CreateCompileResponse
        )
        return output_model

    @staticmethod
    async def read(project_id, compile_id):
        output_model = await validate_models(
            mcp, 'read_compile', 
            {'projectId': project_id, 'compileId': compile_id}, 
            ReadCompileResponse
        )
        return output_model

    @staticmethod
    async def wait_for_job_to_complete(project_id, compile_id):
        attempts = 0
        while attempts < 15:
            attempts += 1
            response = await Compile.read(project_id, compile_id)
            if response.state.value != 'InQueue':
                return response
            sleep(2)
        assert False, "Compile job stuck in queue."


# Test suite:
class TestCompile:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_compile(self, language):
        # Create a project.
        project_id = (await Project.create(language=language)).projectId
        # Test if we can compile the project.
        compile_response = await Compile.create(project_id)
        # Test if the project Id is correct.
        assert compile_response.projectId == project_id
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_create_compile_with_invalid_args(self):
        # Try to compile a project without providing the project Id.
        tool_name = 'create_compile'
        await ensure_request_raises_validation_error(
            tool_name, CreateCompileRequest, {}
        )
        # Try to compile a project that doesn't exist.
        await ensure_request_fails(mcp, tool_name, {'projectId': -1})

    @pytest.mark.asyncio
    async def test_read_compile(self):
        # Create a project and add it to the compile queue.
        project_id = (await Project.create()).projectId
        compile_id = (await Compile.create(project_id)).compileId
        # Test if we can read the compile job.
        compile_response = await Compile.wait_for_job_to_complete(
            project_id, compile_id
        )
        # Test if the compile Id is correct.
        assert compile_response.compileId == compile_id
        assert compile_response.logs
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_read_compile_with_invalid_args(self):
        # Create a project and add it to the compile queue.
        project_id = (await Project.create()).projectId
        compile_id = (await Compile.create(project_id)).compileId
        # Test the invalid requests.
        tool_name = 'read_compile'
        minimal_payload = {'projectId': project_id, 'compileId': compile_id}
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, ReadCompileRequest, minimal_payload
        )
        # Try to read the compile job for a project that doesn't exist.
        await ensure_request_fails(
            mcp, tool_name, minimal_payload | {'projectId': -1}
        )
        # Delete the project to clean up.
        await Project.delete(project_id)
