import pytest
import os
from time import sleep
import requests
from zipfile import ZipFile
from io import BytesIO

from main import mcp
from utils import (
    validate_models, 
    ensure_request_fails, 
    ensure_request_raises_validation_error,
    ensure_request_raises_validation_error_when_omitting_an_arg,
    create_timestamp,
)
from models import (
    ObjectStoreBinaryFile,
    GetObjectStorePropertiesRequest,
    GetObjectStoreJobIdRequest,
    GetObjectStoreURLRequest,
    ListObjectStoreRequest,
    DeleteObjectStoreRequest,
    GetObjectStorePropertiesResponse,
    GetObjectStoreResponse,
    ListObjectStoreResponse,
    RestResponse
)

# Load the organization Id from the environment variables.
ORGANIZATION_ID = os.getenv('QUANTCONNECT_ORGANIZATION_ID')


# Static helpers for common operations:
class ObjectStore:

    @staticmethod
    async def upload(organization_id, key, object_data):
        await validate_models(
            mcp, 'upload_object', 
            {
                'organizationId': organization_id, 
                'key': key, 
                'objectData': object_data
            },
            RestResponse
        )

    @staticmethod
    async def read_properties(organization_id, key):
        output_model = await validate_models(
            mcp, 'read_object_properties', 
            {'organizationId': organization_id, 'key': key}, 
            GetObjectStorePropertiesResponse
        )
        return output_model.metadata

    @staticmethod
    async def read_job_id(organization_id, keys):
        output_model = await validate_models(
            mcp, 'read_object_store_file_job_id', 
            {'organizationId': organization_id, 'keys': keys}, 
            GetObjectStoreResponse
        )
        return output_model.jobId

    @staticmethod
    async def read_download_url(organization_id, job_id):
        return await validate_models(
            mcp, 'read_object_store_file_download_url', 
            {'organizationId': organization_id, 'jobId': job_id}, 
            GetObjectStoreResponse
        )

    @staticmethod
    async def list(organization_id, **kwargs):
        return await validate_models(
            mcp, 'list_object_store_files', 
            {'organizationId': organization_id} | kwargs, 
            ListObjectStoreResponse
        )

    @staticmethod
    async def delete(organization_id, key):
        await validate_models(
            mcp, 'delete_object', 
            {'organizationId': organization_id, 'key': key}, RestResponse
        )

    @staticmethod
    async def wait_for_job_to_complete(organization_id, job_id):
        attempts = 0
        while attempts < 36:
            attempts += 1
            output_model = await ObjectStore.read_download_url(
                organization_id, job_id
            )
            if output_model.url:
                return output_model
            sleep(5)
        assert False, "Download job didn't complete in time."


# Test suite:
class TestObjectStore:

    async def _create_key(self):
        return f'test_key_{create_timestamp()}'

    async def _create_object_data(self, type_=str):
        match type_:
            case t if t is str:
                return "Hello, world!"
            case t if t is bytes:
                return bytes("Hello, world!", encoding="utf-8")

    async def _decode_object_data(self, data, type_=str):
        match type_:
            case t if t is str:
                return data.decode('utf-8')
            case t if t is bytes:
                return data

    @pytest.mark.asyncio
    @pytest.mark.parametrize('type_', [str, bytes])
    async def test_upload(self, type_):
        # Try to upload a file.
        key = await self._create_key()
        await ObjectStore.upload(
            ORGANIZATION_ID, key, await self._create_object_data(type_)
        )
        # Delete the file to clean up.
        await ObjectStore.delete(ORGANIZATION_ID, key)

    @pytest.mark.asyncio
    async def test_upload_with_invalid_args(self):
        # Test the invalid requests.
        tool_name = 'upload_object'
        class_ = ObjectStoreBinaryFile
        minimal_payload = {
            'organizationId': ORGANIZATION_ID, 
            'key': await self._create_key(), 
            'objectData': await self._create_object_data()
        }
        # Try to upload the file without providing all the required
        # data.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        # Try to upload the file to an organization that doesn't exist.
        await ensure_request_fails(
            mcp, tool_name, minimal_payload | {'organizationId': ' '}
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize('type_', [str, bytes])
    async def test_read_metadata(self, type_):
        # Upload a file.
        key = await self._create_key()
        object_data = await self._create_object_data(type_)
        await ObjectStore.upload(ORGANIZATION_ID, key, object_data)
        # Try to read the file properties.
        properties = await ObjectStore.read_properties(ORGANIZATION_ID, key)
        assert properties.key == key
        assert properties.size == len(object_data)
        assert properties.md5 == '6cd3556deb0da54bca060b4c39479839'
        assert properties.mime == 'text/plain'
        match type_:
            case t if t is str:
                assert properties.preview == object_data
            case t if t is bytes:
                assert properties.preview == object_data.decode()
        # Delete the file to clean up.
        await ObjectStore.delete(ORGANIZATION_ID, key)

    @pytest.mark.asyncio
    async def test_read_metadata_with_invalid_args(self):
        tool_name = 'read_object_properties'
        class_ = GetObjectStorePropertiesRequest
        minimal_payload = {
            'organizationId': ORGANIZATION_ID, 
            'key': await self._create_key(),
        }
        # Try to read the file properties without providing all the 
        # required data.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            tool_name, class_, minimal_payload
        )
        # Try to read the file properties from an organization 
        # that doesn't exist.
        await ensure_request_fails(
            mcp, tool_name, minimal_payload | {'organizationId': ' '}
        )
        # Try to read the file properties with a key that doesn't exist
        # in the Object Store.
        await ensure_request_fails(mcp, tool_name, minimal_payload)

    @pytest.mark.asyncio
    @pytest.mark.parametrize('type_', [str, bytes])
    async def test_list_object_store_files(self, type_):
        # Create a directory tree like this:
        # 
        #   root_directory/
        #   ├── child_file
        #   └── child_directory/
        #       └── grandchild_file
        #
        # 1) Define the root directory name.
        root_dir = await self._create_key()
        # 2) Upload the `child_file`
        await ObjectStore.upload(
            ORGANIZATION_ID, 
            f'{root_dir}/child_file', 
            await self._create_object_data(type_)
        )
        # 3) Upload the `grandchild_file`
        await ObjectStore.upload(
            ORGANIZATION_ID, 
            f'{root_dir}/child_directory/grandchild_file', 
            await self._create_object_data(type_)
        )
        # Try to list the files in the Object Store.
        response = await ObjectStore.list(ORGANIZATION_ID)
        assert response.path == '/'
        assert response.objects
        assert [
            (
                obj.key == '/' + root_dir and 
                obj.name == root_dir and 
                obj.mime == 'directory' and 
                obj.folder
            )
            for obj in response.objects
        ]
        # Try to list the contents of the `root_dir`.
        response = await ObjectStore.list(ORGANIZATION_ID, path=root_dir)
        assert response.path == root_dir
        assert len(response.objects) == 2
        assert [
            (
                obj.key == f'/{root_dir}/child_file' and 
                obj.name == 'child_file' and 
                obj.mime == 'text/plain' and 
                not obj.folder
            )
            for obj in response.objects
        ]
        assert [
            (
                obj.key == f'/{root_dir}/child_directory' and 
                obj.name == 'child_directory' and 
                obj.mime == 'directory' and 
                obj.folder
            )
            for obj in response.objects
        ]
        # Try to list the contents of the `child_directory`.
        path = f'{root_dir}/child_directory'
        response = await ObjectStore.list(ORGANIZATION_ID, path=path)
        assert response.path == path
        assert len(response.objects) == 1
        obj = response.objects[0]
        assert (
            obj.key == f'{path}/grandchild_file' and 
            obj.name == 'grandchild_file' and 
            obj.mime == 'text/plain' and 
            not obj.folder
        )
        # Delete the directory tree to clean up.
        await ObjectStore.delete(ORGANIZATION_ID, root_dir)

    @pytest.mark.asyncio
    async def test_list_object_store_files_with_invalid_args(self):
        tool_name = 'list_object_store_files'
        # Try to read the list the Object Store files without providing
        # all the required data.
        await ensure_request_raises_validation_error(
            tool_name, ListObjectStoreRequest, {}
        )
        # Try to list the Object Store files in an organization that 
        # doesn't exist.
        await ensure_request_fails(mcp, tool_name, {'organizationId': ' '})

    @pytest.mark.asyncio
    @pytest.mark.parametrize('type_', [str, bytes])
    async def test_read_object_store_file_job_id(self, type_):
        # Upload a file.
        key = await self._create_key()
        await ObjectStore.upload(
            ORGANIZATION_ID, key, await self._create_object_data(type_)
        )
        # Try to read the job Id.
        await ObjectStore.read_job_id(ORGANIZATION_ID, [key])
        # Delete the file to clean up.
        await ObjectStore.delete(ORGANIZATION_ID, key)

    @pytest.mark.asyncio
    async def test_read_object_store_file_job_id_with_invalid_args(self):
        # Try to read the job Id without providing all the required 
        # data.
        await ensure_request_raises_validation_error_when_omitting_an_arg(
            'read_object_store_file_job_id', GetObjectStoreJobIdRequest, 
            {
                'organizationId': ORGANIZATION_ID,
                'keys': [await self._create_key()]
            }
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize('type_', [str, bytes])
    async def test_read_object_store_file_download_url(self, type_):
        # Upload a file.
        key = await self._create_key()
        object_data = await self._create_object_data(type_)
        await ObjectStore.upload(ORGANIZATION_ID, key, object_data)
        # Try to get the download URL.
        job_id = await ObjectStore.read_job_id(ORGANIZATION_ID, [key])
        url = (
            await ObjectStore.wait_for_job_to_complete(ORGANIZATION_ID, job_id)
        ).url
        # Ensure the content in the downloaded file matches the 
        # upload.
        response = requests.get(url)
        response.raise_for_status()
        #  1) Unzip the zip file.
        with ZipFile(BytesIO(response.content), 'r') as zip_ref:
            #  2) In the zip file, open the object file.
            with zip_ref.open(key) as file:
                #  3) Check if the file contents are correct.
                assert object_data == await self._decode_object_data(
                    file.read(), type_
                )
        # Delete the file to clean up.
        await ObjectStore.delete(ORGANIZATION_ID, key)
