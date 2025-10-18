import time
import docker

from organization_workspace import OrganizationWorkspace
from api_connection import USER_ID, API_TOKEN

def test_organization_workspace_mount():
    # Ensure the MOUNT_SOURCE environment variable is set.
    assert OrganizationWorkspace.MOUNT_SOURCE, 'MOUNT_SOURCE env var is not set.'
    # Create a Docker client.
    client = docker.from_env()
    # Start MCP Server inside a container.
    container = client.containers.run(
        image='quantconnect/mcp-server',
        environment={
            'QUANTCONNECT_USER_ID': USER_ID,
            'QUANTCONNECT_API_TOKEN': API_TOKEN
        },
        platform='linux/amd64',
        volumes={
            OrganizationWorkspace.MOUNT_SOURCE: {
                'bind': OrganizationWorkspace.MOUNT_DESTINATION, 'mode': 'ro'}
            },
        detach=True,  # Run in background
        auto_remove=True  # Equivalent to --rm
    )
    # Wait for the container to start running.
    time.sleep(5)
    # Check if the expected mount exists.
    assert any(
        mount['Type'] == 'bind' and
        mount['Source'] == OrganizationWorkspace.MOUNT_SOURCE and
        mount['Destination'] == OrganizationWorkspace.MOUNT_DESTINATION and
        mount['Mode'] == 'ro'
        for mount in container.attrs['Mounts']
    )
    # Stop the container.
    container.stop()
