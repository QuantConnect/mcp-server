import pytest
import json

from main import mcp
from test_project import Project
from test_compile import Compile
from test_project_collaboration import ProjectCollaboration, COLLABORATOR_ID
from utils import (
    validate_models, 
    ensure_request_raises_validation_error,
    ensure_request_raises_validation_error_when_omitting_an_arg,
    ensure_request_fails_when_including_an_invalid_arg
)
from models import (
    CreateProjectFileRequest,
    ReadFilesRequest,
    UpdateFileNameRequest,
    UpdateFileContentsRequest,
    DeleteFileRequest,
    RestResponse,
    ProjectFilesResponse
)

# Static helpers for common operations:
class Files:

    @staticmethod
    async def create(project_id, name, **kwargs):
        return await validate_models(
            mcp, 'create_file', 
            {'projectId': project_id, 'name': name} | kwargs,
            ProjectFilesResponse
        )

    @staticmethod
    async def read(project_id, **kwargs):
        return await validate_models(
            mcp, 'read_file', {'projectId': project_id} | kwargs, 
            ProjectFilesResponse
        )

    @staticmethod
    async def update(project_id, **kwargs):
        tool_name = 'update_file_'
        if 'content' in kwargs:
            tool_name += 'contents'
            output_class = ProjectFilesResponse
        else:
            tool_name += 'name'
            output_class = RestResponse
        output_model = await validate_models(
            mcp, tool_name, {'projectId': project_id} | kwargs, output_class
        )
        return output_model

    @staticmethod
    async def delete(project_id, name):
        return await validate_models(
            mcp, 'delete_file', {'projectId': project_id, 'name': name},
            RestResponse
        )

    @staticmethod
    async def setup_project(language, algorithm=None):
        # Create a project.
        project_id = (await Project.create(language=language)).projectId
        if algorithm:
            # Read the algorithm file.
            with open('algorithms/' + algorithm, 'r') as file:
                content = file.read()
            # Update the project to the new algorithm.
            await Files.update(
                project_id, 
                name='main.py' if language == 'Py' else 'Main.cs', 
                content=content
            )
        # Compile the project.
        compile_id = (await Compile.create(project_id)).compileId
        await Compile.wait_for_job_to_complete(project_id, compile_id)
        return project_id, compile_id


# Test suite:
class TestFiles:

    _basic_code_file = {
        'Py': """class CustomClass:
    def __init__(self):
        pass""",

        'C#': """public class CustomClass 
{
    CustomClass() 
    {

    }
}"""
    }

    _basic_research_file = {
        'Py': {
          'cells': [
            {
              'cell_type': 'code',
              'execution_count': None,
              'metadata': {
                'pycharm': {
                  'name': '#%%\n'
                }
              },
              'outputs': [
                
              ],
              'source': [
                "print('Hello world!')\n",
              ]
            }
          ],
          'metadata': {
            'kernelspec': {
              'display_name': 'Python 3',
              'language': 'python',
              'name': 'python3'
            },
            'language_info': {
              'codemirror_mode': {
                'name': 'ipython',
                'version': 3
              },
              'file_extension': '.py',
              'mimetype': 'text/x-python',
              'name': 'python',
              'nbconvert_exporter': 'python',
              'pygments_lexer': 'ipython3',
              'version': '3.6.8'
            }
          },
          'nbformat': 4,
          'nbformat_minor': 2
        },

        'C#': {
          "cells": [
            {
              "cell_type": "code",
              "execution_count": 1,
              "metadata": {
                
              },
              "outputs": [
                
              ],
              "source": [
                "// We need to load assemblies at the start in their own cell\n",
                "#load \"../Initialize.csx\""
              ]
            },
          ],
          "metadata": {
            "kernelspec": {
              "display_name": ".NET (C#)",
              "language": "C#",
              "name": "csharp"
            },
            "language_info": {
              "file_extension": ".cs",
              "mimetype": "text/x-csharp",
              "name": "C#",
              "pygments_lexer": "csharp",
              "version": "9.0"
            }
          },
          "nbformat": 4,
          "nbformat_minor": 2
        }
    }

    _default_file_names = {
        'Py': ['main.py', 'research.ipynb'],
        'C#': ['Main.cs', 'Research.ipynb']
    }

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_file(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Test adding an empty code file to the project.
        await Files.create(
            id_, 'test_file_1.py' if language == 'Py' else 'TestFile1.cs'
        )
        # Test adding a code file with contents to the project.
        if language == 'Py':
            name = 'test_file_2.py'
        else:
            name = 'TestFile2.cs'
        content = self._basic_code_file[language]
        file = (await Files.create(id_, name, content=content)).files[0]
        assert file.name == name
        assert file.content == content
        # Test adding a research file with contents to the project. 
        if language == 'Py':
            name = 'test_file_3.py'
        else:
            name = 'TestFile3.ipynb'
        content = json.dumps(self._basic_research_file[language])
        file = (await Files.create(id_, name, content=content)).files[0]
        assert file.name == name
        assert file.content == content
        # Test adding a directory.
        if language == 'Py':
            name = 'test_dir/test_file_4.py'
        else:
            name = 'TestDir/TestFile4.cs'
        await Files.create(id_, name)  # Response is {'success': True}
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    async def test_create_file_during_project_collaboration(self):
        # Create a project and add a collaborator.
        project_id = (await Project.create()).projectId
        await ProjectCollaboration.create(
            project_id, COLLABORATOR_ID, True, True
        )
        # Before editing the project, lock it and read files to avoid
        # errors. 
        await ProjectCollaboration.lock(project_id)
        await Files.read(project_id)
        # Test adding a file to the project.
        await Files.create(project_id, 'test_file_1.py')
        # Remove the collaborator and delete the project to clean up.
        await ProjectCollaboration.delete(project_id, COLLABORATOR_ID)
        await Project.delete(project_id)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_create_file_on_with_invalid_args(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Test the invalid requests.
        tool_name = 'create_file'
        minimal_payload = {
            'projectId': id_, 
            'name': 'test_file.py' if language == 'Py' else 'TestFile.cs'
        }
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, CreateProjectFileRequest, minimal_payload
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to add a file to a project that doesn't exist.
                {'projectId': -1},
                # Try to add a file to a project with the same name as 
                # a file that is already in the project.
                {'name': self._default_file_names[language][0]},
                # Try to add a file that has no content.
                {'content': ''}
            ]
        )
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_read_file(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Try to read all the default files in the project one-by-one.
        for file_name in self._default_file_names[language]:
            files = (await Files.read(id_, name=file_name)).files
            assert len(files) == 1
            file = files[0]
            assert file.projectId == id_
            assert file.name == file_name
        # Try to read all the default files in a project at once.
        files = (await Files.read(id_)).files
        assert len(files) == 2
        for f in files:
            assert f.projectId == id_
            assert f.name in self._default_file_names[language]
        # Try to read all the files after adding a new empty file to 
        # the project.
        if language == 'Py':
            name = 'test_dir/test_file.py'
        else:
            name = 'TestDir/TestFile.cs'
        content = self._basic_code_file[language]
        await Files.create(id_, name, content=content)
        files = (await Files.read(id_, name=name)).files
        assert len(files) == 1
        file = files[0]
        assert file.name == name
        assert file.content == content
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_read_file_with_invalid_args(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Test the invalid requests.
        tool_name = 'read_file'
        # Try to read the files of a project without providing the 
        # project Id.
        await ensure_request_raises_validation_error(
            tool_name, ReadFilesRequest, {}
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, {'projectId': id_}, [
                # Try to read a file from a project that doesn't exist.
                {'projectId': -1},
                # Try to read a file that doesn't exist.
                {'name': self._default_file_names[language][0][2:]},
            ]
        )
        # Delete the project to clean up.
        await Project.delete(id_)


    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_update_file_name(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Add a basic code file.
        name = 'test_file.py' if language == 'Py' else 'TestFile.cs'
        await Files.create(id_, name)
        # Try to update the file name.
        new_name = 'test_file_1.py' if language == 'Py' else 'TestFile1.cs'
        await Files.update(id_, name=name, newName=new_name)
        files = (await Files.read(id_)).files
        assert all([f.name != name for f in files])
        assert any([f.name == new_name for f in files])
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_update_file_name_with_invalid_args(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Add a basic code file.
        name = 'test_file.py' if language == 'Py' else 'TestFile.cs'
        await Files.create(id_, name)
        # Test the invalid requests.
        tool_name = 'update_file_name'
        minimal_payload = {
            'projectId': id_, 
            'name': name, 
            'newName': 'test_file_1.py' if language == 'Py' else 'TestFile1.cs'
        }
        # Try to update the file name without providing all the data.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, UpdateFileNameRequest, minimal_payload
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to update the name of a file in a project that 
                # doesn't exist.
                {'projectId': -1},
                # Try to update the name of a file that doesn't exist
                # in the project.
                {'name': self._default_file_names[language][0][2:]},
            ]
        )
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_update_contents(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Update the contents of the default code file.
        name = self._default_file_names[language][0]
        content = self._basic_code_file[language]
        response = await Files.update(id_, name=name, content=content)
        assert len(response.files) == 1
        file = response.files[0]
        assert file.name == name
        assert file.content == content
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_update_file_contents_with_invalid_args(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Test the invalid requests.
        tool_name = 'update_file_contents'
        minimal_payload = {
            'projectId': id_, 
            'name': self._default_file_names[language][0], 
            'content': self._basic_code_file[language]
        }
        # Try to update the contents of a file without providing all
        # the data.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, UpdateFileContentsRequest, minimal_payload
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to contents of a file in a project that doesn't 
                # exist.
                {'projectId': -1},
                # Try to update a file that doesn't exist in the 
                # project.
                {'name': self._default_file_names[language][0][2:]},
                # Try to update the file contents to a blank file.
                {'content': ''},
            ]
        )
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_delete_file(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Try to delete the code file.
        await Files.delete(id_, self._default_file_names[language][0])
        files = (await Files.read(id_)).files
        assert len(files) == 1
        assert files[0].name == self._default_file_names[language][1]
        # Try to delete the research file.
        await Files.delete(id_, self._default_file_names[language][1])
        files = (await Files.read(id_)).files
        assert len(files) == 0
        # Try to delete a file in a directory.
        if language == 'Py':
            name = 'test_dir/test_file.py'
        else:
            name = 'TestDir/TestFile.cs'
        content = self._basic_code_file[language]
        await Files.create(id_, name, content=content)
        await Files.delete(id_, name)
        files = (await Files.read(id_)).files
        assert len(files) == 0
        # Delete the project to clean up.
        await Project.delete(id_)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('language', ['Py', 'C#'])
    async def test_delete_file_with_invalid_args(self, language):
        # Create a project.
        id_ = (await Project.create(language=language)).projectId
        # Test the invalid requests.
        tool_name = 'delete_file'
        minimal_payload = {
            'projectId': id_, 
            'name': self._default_file_names[language][0]
        }
        # Try to read a file without providing all the required data.
        await ensure_request_raises_validation_error(
            tool_name, DeleteFileRequest, {}
        )
        await ensure_request_fails_when_including_an_invalid_arg(
            mcp, tool_name, minimal_payload, [
                # Try to delete a file from a project that doesn't exist.
                {'projectId': -1},
                # Try to delete a file that doesn't exist.
                {'name': self._default_file_names[language][0][2:]},
            ]
        )
        # Delete the project to clean up.
        await Project.delete(id_)
