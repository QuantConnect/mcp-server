import pytest
from time import sleep

from main import mcp
from test_project import Project
from test_files import Files
from test_compile import Compile
from utils import (
    validate_models, 
    ensure_request_fails, 
    ensure_request_raises_validation_error,
    ensure_request_raises_validation_error_when_omitting_an_arg,
    ensure_request_fails_when_including_an_invalid_arg
)
from models import (
    CreateBacktestRequest,
    ReadBacktestRequest,
    UpdateBacktestRequest,
    DeleteBacktestRequest,
    ListBacktestRequest,
    BacktestResponse,
    BacktestSummaryResponse,
    RestResponse
)


# Static helpers for common operations:
class Backtest:

    @staticmethod
    async def create(
            project_id, compile_id, backtest_name='Test Backtest', **kwargs):
        output_model = await validate_models(
            mcp, 'create_backtest', 
            {
                'projectId': project_id, 
                'compileId': compile_id, 
                'backtestName': backtest_name
            } | kwargs,
            BacktestResponse
        )
        return output_model.backtest

    @staticmethod
    async def read(project_id, backtest_id):
        output_model = await validate_models(
            mcp, 'read_backtest', 
            {'projectId': project_id, 'backtestId': backtest_id}, 
            BacktestResponse
        )
        return output_model.backtest

    @staticmethod
    async def update(project_id, backtest_id, **kwargs):
        output_model = await validate_models(
            mcp, 'update_backtest', 
            {'projectId': project_id, 'backtestId': backtest_id} | kwargs, 
            RestResponse
        )
        return output_model

    @staticmethod
    async def delete(project_id, backtest_id):
        output_model = await validate_models(
            mcp, 'delete_backtest', 
            {'projectId': project_id, 'backtestId': backtest_id}, 
            RestResponse
        )
        return output_model

    @staticmethod
    async def list(project_id, **kwargs):
        output_model = await validate_models(
            mcp, 'list_backtests', {'projectId': project_id} | kwargs, 
            BacktestSummaryResponse
        )
        return output_model.backtests

    @staticmethod
    async def wait_for_job_to_complete(project_id, backtest_id):
        attempts = 0
        while attempts < 5:
            attempts += 1
            backtest = await Backtest.read(project_id, backtest_id)
            if backtest.completed:
                return 
            sleep(10)
        assert False, "Backtest job didn't complete in time."

    @staticmethod
    async def run_algorithm(language, algo=None, wait_to_complete=True):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language, algo)
        # Run the backtest.
        backtest_id = (await Backtest.create(project_id, compile_id)).backtestId
        if wait_to_complete:
            await Backtest.wait_for_job_to_complete(project_id, backtest_id)
        return project_id, backtest_id


# Test suite:
class TestBacktest:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_backtest(self, language):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language)
        # Try to run the backtest.
        name = 'Test Backtest'
        backtest = await Backtest.create(project_id, compile_id, name)
        assert backtest.name == name
        assert backtest.projectId == project_id
        assert backtest.parameterSet == []
        # Try to run the backtest with some parameters.
        await Backtest.create(
            project_id, compile_id, name, 
            parameters={'a': 0, 'b': 0.0, 'c': 'foo'}
        )
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_backtest_with_invalid_args(self, language):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language)
        # Test the invalid requests.
        tool_name = 'create_backtest'
        class_ = CreateBacktestRequest
        minimal_payload = {
            'projectId': project_id,
            'compileId': compile_id,
            'backtestName': 'Test backtest'
        }
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to backtest a project that doesn't exist.
                {'projectId': -1},
                # Try to run a backtest with a compile Id that doesn't
                # exist.
                {'compileId': ' '}
            ]
        )
        # Try to create a backtest with unsupported data types for the
        # parameters (in this case, the value is a dictionary).
        await ensure_request_raises_validation_error(
            tool_name, class_, 
            minimal_payload | {'parameters': {'p': {'k': 'v'}}}
        )
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_read_backtest(self, language):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language)
        # Start a backtest.
        parameters = {'a': 0, 'b': 0.0, 'c': 'foo'}
        backtest = await Backtest.create(
            project_id, compile_id, parameters=parameters
        )
        backtest_id = backtest.backtestId
        # Try to read the backtest result.
        backtest = await Backtest.read(project_id, backtest_id)
        assert backtest.projectId == project_id
        assert backtest.backtestId == backtest_id
        assert backtest.parameterSet == parameters
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_read_backtest_with_invalid_args(self, language):
        # Start a backtest.
        project_id, backtest_id = await Backtest.run_algorithm(language)
        # Test the invalid requests.
        tool_name = 'read_backtest'
        class_ = ReadBacktestRequest
        minimal_payload = {'projectId': project_id, 'backtestId': backtest_id}
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        # Try to read a backtest that doesn't exist.
        await ensure_request_fails(
            mcp, tool_name, minimal_payload | {'backtestId': ' '}
        )
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_list_backtests(self, language):
        # Start a backtest.
        project_id, backtest_id = await Backtest.run_algorithm(language)
        # Try to list all the backtest when there is just 1 backtest.
        backtests = await Backtest.list(project_id)
        assert len(backtests) == 1
        backtest = backtests[0]
        assert backtest.backtestId == backtest_id
        # Start a second backtest.
        compile_id = (await Compile.create(project_id)).compileId
        await Compile.wait_for_job_to_complete(project_id, compile_id)
        backtest_ids = [
            backtest_id, 
            (await Backtest.create(project_id, compile_id)).backtestId
        ]
        # Try to list all the backtests when there are multiple 
        # backtests.
        backtests = await Backtest.list(project_id)
        assert len(backtests) == 2
        assert len(set([backtest.backtestId for backtest in backtests])) == 2
        for backtest in backtests:
            assert backtest.backtestId in backtest_ids
        # Try to list all the backtests with statistics included.
        await Backtest.wait_for_job_to_complete(project_id, backtest_ids[-1])
        backtests = await Backtest.list(project_id, includeStatistics=True)
        assert len(backtests) == 2
        assert len(set([backtest.backtestId for backtest in backtests])) == 2
        for backtest in backtests:
            assert backtest.backtestId in backtest_ids
            assert backtest.alpha is not None
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_list_backtests_with_invalid_args(self):
        tool_name = 'list_backtests'
        # Try to list all the backtests without providing the project 
        # Id.
        await ensure_request_raises_validation_error(
            tool_name, ListBacktestRequest, {}
        )
        # Try to list all the backtests of a project that doesn't
        # exist.
        await ensure_request_fails(mcp, tool_name, {'projectId': -1})

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        'language, algo', 
        [
            ('Py', 'runtime_error.py'),
            ('C#', 'RuntimeError.cs')
        ]
    )
    async def test_list_backtests_with_runtime_error(self, language, algo):
        # Run the backtest.
        project_id, _ = await Backtest.run_algorithm(language, algo)
        # Try to list the backtest of the project.
        await Backtest.list(project_id)
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_update_backtest(self, language):
        # Start a backtest.
        project_id, backtest_id = await Backtest.run_algorithm(
            language, wait_to_complete=False
        )
        # Try to update the backtest name and note.
        name = 'new name'
        note = 'new note'
        await Backtest.update(project_id, backtest_id, name=name, note=note)
        backtest = await Backtest.read(project_id, backtest_id)
        assert backtest.name == name
        assert backtest.note == note
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_update_backtest_with_invalid_args(self, language):
        # Start a backtest.
        project_id, backtest_id = await Backtest.run_algorithm(
            language, wait_to_complete=False
        )
        # Test the invalid requests.
        tool_name = 'update_backtest'
        class_ = UpdateBacktestRequest
        minimal_payload = {'projectId': project_id, 'backtestId': backtest_id}
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to update a backtest in a project that doesn't 
                # exist.
                {'projectId': -1},
                # Try to update a backtest that doesn't exist.
                {'backtestId': ' '}
            ]
        )
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_delete_backtest(self, language):
        # Start a backtest.
        project_id, backtest_id = await Backtest.run_algorithm(
            language, wait_to_complete=False
        )
        # Try to delete the backtest.
        await Backtest.delete(project_id, backtest_id)
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_delete_backtest_with_invalid_args(self, language):
        # Start a backtest.
        project_id, backtest_id = await Backtest.run_algorithm(
            language, wait_to_complete=False
        )
        # Test the invalid requests.
        tool_name = 'delete_backtest'
        class_ = DeleteBacktestRequest
        minimal_payload = {'projectId': project_id, 'backtestId': backtest_id}
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        # Try to delete a backtest from a project that doesn't exist.
        await ensure_request_fails(
            mcp, tool_name, minimal_payload | {'projectId': -1}
        )
        # Delete the project to clean up.
        await Project.delete(project_id)
