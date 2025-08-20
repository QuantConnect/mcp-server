import pytest

from main import mcp
from utils import validate_models
from models import (
    BacktestInitResponse,
    CodeCompletionResponse,
    ErrorEnhanceResponse,
    PEP8ConvertResponse,
    SyntaxCheckResponse,
    SearchResponse
)


# Static helpers for common operations:
class AI:

    @staticmethod
    async def check_initialization_errors(language, files):
        return await validate_models(
            mcp, 'check_initialization_errors', 
            {'language': language, 'files': files}, BacktestInitResponse
        )

    @staticmethod
    async def complete_code(language, sentence, **kwargs):
        return await validate_models(
            mcp, 'complete_code', 
            {'language': language, 'sentence': sentence} | kwargs, 
            CodeCompletionResponse
        )

    @staticmethod
    async def enhance_error_message(language, message, **kwargs):
        return await validate_models(
            mcp, 'enhance_error_message', 
            {
                'language': language, 
                'error': {'message': message} | kwargs
            }, 
            ErrorEnhanceResponse
        )

    @staticmethod
    async def update_code_to_pep8(files):
        return await validate_models(
            mcp, 'update_code_to_pep8', {'files': files}, PEP8ConvertResponse
        )

    @staticmethod
    async def check_syntax(language, files):
        return await validate_models(
            mcp, 'check_syntax', {'language': language, 'files': files}, 
            SyntaxCheckResponse
        )

    @staticmethod
    async def search_quantconnect(language, criteria):
        return await validate_models(
            mcp, 'search_quantconnect', {'language': language, 'criteria': criteria}, 
            SearchResponse
        )
        

# Test suite:
class TestAI:

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, algo, name', [
        ('Py', 'initialization_errors.py', 'main.py'),
        ('C#', 'InitializationErrors.cs', 'Main.cs')
    ])
    async def test_check_initialization_errors(self, language, algo, name):
        # Get the file content.
        with open('algorithms/' + algo, 'r') as file:
            content = file.read()
        # Check for initialization errors.
        await AI.check_initialization_errors(
            language, [{'name': name, 'content': content}]
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language, sentence, answer', [
        ('Py', 'self.add_e', 'self.add_equity'),
        ('C#', 'AddE', 'AddEquity')
    ])
    async def test_complete_code(self, language, sentence, answer):
        response = await AI.complete_code(language, sentence)
        assert response.payload
        assert any([answer in c for c in response.payload])

    @pytest.mark.asyncio
    async def test_enhance_error_message(self):
        message = """  at initialize
        self._option = self.add_index_option("SPX", Resolution.MINUTE, "SPXW").symbol
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    in c1afe80a-e056-4841-b0c1-d9c562cf2bd8.py: line 15
    The specified market wasn't found in the markets lookup. Requested: spxw. You can add markets by calling QuantConnect.Market.Add(string,int) (Parameter 'market')
        """
        await AI.enhance_error_message('Py', message)

    @pytest.mark.asyncio
    async def test_update_code_to_pep8(self):
        name = 'pep8_violations.py'
        # Get the file content.
        with open('algorithms/' + name, 'r') as file:
            content = file.read()
        files = [{'name': name, 'content': content}]
        response = await AI.update_code_to_pep8(files)
        new_content = response.payload[name]
        for x in ['Initialize', 'AddEquity']:
            assert x not in new_content
        for x in ['initialize', 'add_equity']:
            assert x in new_content
        
    @pytest.mark.asyncio
    async def test_check_syntax(self):
        name = 'syntax_errors.py'
        # Get the file content.
        with open('algorithms/' + name, 'r') as file:
            content = file.read()
        files = [{'name': name, 'content': content}]
        response = await AI.check_syntax('Py', files)
        assert response.state.value == 'Error'
        assert response.payload

    @pytest.mark.asyncio
    async def test_search_quantconnect(self):
        criteria = [
            {
                'input': 'How to create an Alpha model',
                'type': 'Examples',
                'count': 3
            }
        ]
        response = await AI.search_quantconnect('Py', criteria)
        assert response.state.value == 'End'
        assert len(response.retrivals) == 3
        
