from __init__ import __version__

import httpx
from base64 import b64encode
from hashlib import sha256
from time import time
import os
from pydantic_core import to_jsonable_python

# The QuantConnect API the server calls; set QUANTCONNECT_API_URL to use another deployment of it.
BASE_URL = os.getenv('QUANTCONNECT_API_URL', 'https://www.quantconnect.com/api/v2').rstrip('/')

# Load credentials from environment variables.
USER_ID = os.getenv('QUANTCONNECT_USER_ID')
API_TOKEN = os.getenv('QUANTCONNECT_API_TOKEN')

def get_headers():
    # Get timestamp
    timestamp = f'{int(time())}'
    time_stamped_token = f'{API_TOKEN}:{timestamp}'.encode('utf-8')
    # Get hased API token
    hashed_token = sha256(time_stamped_token).hexdigest()
    authentication = f'{USER_ID}:{hashed_token}'.encode('utf-8')
    authentication = b64encode(authentication).decode('ascii')
    # Create headers dictionary.
    return {
        'Authorization': f'Basic {authentication}',
        'Timestamp': timestamp,
        'User-Agent': f'QuantConnect MCP Server v{__version__}'
    }

async def post(endpoint: str, model: object = None, timeout: float = 30.0):
    """Make an HTTP POST request to the API with proper error handling.
    
    Args:
        endpoint: The API endpoint path (ex: '/projects/create')
        model: Optional Pydantics model for the request.
        timeout: Optional timeout for the request (in seconds).
        
    Returns:
        Response JSON if successful. Otherwise, throws an exception, 
        which is handled by the Server class.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f'{BASE_URL}{endpoint}', 
            headers=get_headers(), 
            json=to_jsonable_python(model, exclude_none=True) if model else {}, 
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
