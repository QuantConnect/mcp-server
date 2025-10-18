import pytest
from time import sleep

from main import mcp
from test_project_nodes import ProjectNodes
from test_project import Project
from test_files import Files
from utils import (
    validate_models, 
    ensure_request_fails, 
    ensure_request_raises_validation_error,
    ensure_request_raises_validation_error_when_omitting_an_arg,
    ensure_request_fails_when_including_an_invalid_arg
)
from models import (
    CreateLiveAlgorithmRequest,
    ReadLiveAlgorithmRequest,

    AuthorizeExternalConnectionResponse,
    CreateLiveAlgorithmResponse,
    LiveAlgorithmResults,
    LivePortfolioResponse,
    LiveAlgorithmListResponse,
    RestResponse
)

DEFAULT_SETTINGS = {
    'versionId': '-1', 
    'brokerage': {
        'id': 'QuantConnectBrokerage' 
    }
}


# Static helpers for common operations:
class Live:

    @staticmethod
    async def authorize_connection(brokerage):
        return await validate_models(
            mcp, 'authorize_connection', {'brokerage': brokerage},
            AuthorizeExternalConnectionResponse
        )

    @staticmethod
    async def create(
            project_id, compile_id, node_id, 
            version_id=DEFAULT_SETTINGS['versionId'], 
            brokerage=DEFAULT_SETTINGS['brokerage'], 
            **kwargs):
        return await validate_models(
            mcp, 'create_live_algorithm', 
            {
                'projectId': project_id, 
                'compileId': compile_id, 
                'nodeId': node_id,
                'versionId': version_id,
                'brokerage': brokerage
            } | kwargs,
            CreateLiveAlgorithmResponse
        )

    @staticmethod
    async def read(project_id):
        return await validate_models(
            mcp, 'read_live_algorithm', {'projectId': project_id},
            LiveAlgorithmResults
        )

    @staticmethod
    async def list(**kwargs):
        output_model = await validate_models(
            mcp, 'list_live_algorithms', kwargs, LiveAlgorithmListResponse
        )        
        return output_model.live

    @staticmethod
    async def read_portfolio(project_id):
        output_model = await validate_models(
            mcp, 'read_live_portfolio', {'projectId': project_id},
            LivePortfolioResponse
        )
        return output_model.portfolio

    @staticmethod
    async def liquidate(project_id):
        return await validate_models(
            mcp, 'liquidate_live_algorithm', {'projectId': project_id},
            RestResponse
        )

    @staticmethod
    async def stop(project_id):
        return await validate_models(
            mcp, 'stop_live_algorithm', {'projectId': project_id},
            RestResponse
        )

    async def get_node_id(project_id):
        # Get the Id of a live trading node (CPU node that isn't busy).
        nodes = (await ProjectNodes.read(project_id)).nodes.live
        nodes = [n for n in nodes if not n.busy and not n.hasGpu]
        assert nodes, 'No nodes available'
        return nodes[0].id

    @staticmethod
    async def wait_for_algorithm_to_start(project_id):
        attempts = 0
        while attempts < 18: 
            attempts += 1
            live = await Live.read(project_id)
            if live.status.value == 'Running':
                return live
            sleep(10)
        assert False, "Live job didn't start in time."

    @staticmethod
    async def wait_for_holding_to_be_removed(project_id, symbol_id):
        attempts = 0
        while attempts < 60: # 10 minutes
            attempts += 1
            portfolio = await Live.read_portfolio(project_id)
            if symbol_id not in portfolio.holdings:
                return 
            sleep(10)
        assert False, "Holding wasn't removed in time."

    @staticmethod
    async def wait_for_holdings_to_update(project_id, symbol_id):
        attempts = 0
        while attempts < 60: # 10 minutes
            attempts += 1
            portfolio = await Live.read_portfolio(project_id)
            if symbol_id in portfolio.holdings:
                return portfolio
            sleep(10)
        assert False, "Holding wasn't updated in time."


# Test suite:
class TestLive:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_live_algorithm(self, language):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language)
        # Get the Id of a live trading node.
        node_id = await Live.get_node_id(project_id)
        # Try to deploy the algorithm.
        response = await Live.create(project_id, compile_id, node_id)
        assert response.source == 'api-v2'
        assert response.projectId == project_id
        assert response.live.brokerage == 'PaperBrokerage'
        # Stop the algorithm and delete the project to clean up.
        await Live.stop(project_id)
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_create_live_algorithm_with_invalid_args(self):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project('Py')
        node_id = await Live.get_node_id(project_id)
        # Test the invalid requests.
        tool_name = 'create_live_algorithm'
        class_ = CreateLiveAlgorithmRequest
        minimal_payload = DEFAULT_SETTINGS | {
            'projectId': project_id, 
            'compileId': compile_id, 
            'nodeId': node_id
        }
        # Try to upload the file without providing all the required
        # data.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        # Try to upload the file to an organization that doesn't exist.
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to deploy a project that doesn't exist.
                {'projectId': -1},
                # Try to deploy with a compile Id that doesn't exist.
                {'compileId': ' '},
                # Try to deploy with a node that doesn't exist.
                {'nodeId': ' '},
            ]
        )
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_read_live_algorithm(self, language):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language)
        # Get the Id of a live trading node.
        node_id = await Live.get_node_id(project_id)
        # Deploy the algorithm.
        await Live.create(project_id, compile_id, node_id)
        # Try to read the algorithm
        live = await Live.read(project_id)
        assert live.brokerage == 'PaperBrokerage'
        # Stop the algorithm and delete the project to clean up.
        await Live.stop(project_id)
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_read_live_algorithm_with_invalid_args(self):
        # Test the invalid requests.
        tool_name = 'read_live_algorithm'
        class_ = ReadLiveAlgorithmRequest
        # Try to read the live algorithm w/o providing all the required
        # data.
        await ensure_request_raises_validation_error(tool_name, class_, {})
        # Try to read the live algorithm of a project that doesn't 
        # exist.
        await ensure_request_fails(mcp, tool_name, {'projectId': -1})


    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo', [
        ('Py', 'live_liquidate.py')#, ('C#', 'LiveLiquidate.cs')
    ])
    async def test_read_and_liquidate_portfolio(self, language, algo):
        # Create and compile the project.
        project_id, compile_id = await Files.setup_project(language, algo)
        # Deploy the algorithm with an existing holding, 1 BTCUSD.
        holding = {
            'symbol': 'BTCUSD',
            'symbolId': 'BTCUSD 2XR',
            'quantity': 1,
            'averagePrice': 100_000
        }
        await Live.create(
            project_id, compile_id, await Live.get_node_id(project_id),
            brokerage={'id': 'QuantConnectBrokerage', 'holdings': [holding]}
        )
        # Wait for the algorithm to start running.
        await Live.wait_for_algorithm_to_start(project_id)
        # Ensure the algorithm is invested.
        portfolio = await Live.wait_for_holdings_to_update(
            project_id, holding['symbolId']
        )
        read_holding = portfolio.holdings[holding['symbolId']]
        assert read_holding.a == holding['averagePrice']
        assert read_holding.q ==  holding['quantity']
        # Try to liquidate (and stop) the algorithm.
        await Live.liquidate(project_id)
        # Ensure the algorithm is no longer invested.
        await Live.wait_for_holding_to_be_removed(
            project_id, holding['symbolId']
        )
        # Ensure the algorithm is no longer running.
        live = await Live.read(project_id)
        assert live.stopped is not None
        # Delete the project to clean up.
        await Project.delete(project_id)

    @pytest.mark.asyncio
    async def test_list_live_algorithms(self):
        # Try to list the live algorithms.
        algorithms = await Live.list()
        assert algorithms
        # Try to list the algorithms of a single project.
        id_ = [algo.projectId for algo in algorithms][0]
        algorithms = await Live.list(projectId=id_)
        assert algorithms
        for algo in algorithms:
            assert algo.projectId == id_
        # Try to list the algorithms that have stopped.
        algorithms = await Live.list(status='Stopped')
        assert algorithms
        for algo in algorithms:
            assert algo.status == 'Stopped'

