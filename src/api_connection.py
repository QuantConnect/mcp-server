import httpx
from base64 import b64encode
from hashlib import sha256
from time import time
import os
from pydantic_core import to_jsonable_python
import sys
import traceback

BASE_URL = 'https://www.quantconnect.com/api/v2'

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
        'Timestamp': timestamp
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

    url = f"{BASE_URL}{endpoint}"
    payload = to_jsonable_python(model, exclude_none=True) if model else {}

    # Log the API call
    print("=" * 80, file=sys.stderr)
    print(f"[MCP API] POST {url}", file=sys.stderr)
    print(f"[Request Payload] {payload}", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers=get_headers(), 
                json=payload, 
                timeout=timeout
            )

            print(f"[MCP API Response] Status={response.status_code} Endpoint={endpoint}", file=sys.stderr)
            print(f"[Response Body] {response.text[:500]}{'...' if len(response.text) > 500 else ''}", file=sys.stderr)

            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as http_err:
        print("[ERROR] HTTP status error occurred", file=sys.stderr)
        print(f"Status: {http_err.response.status_code}", file=sys.stderr)
        print(f"Body: {http_err.response.text}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise

    except httpx.RequestError as req_err:
        print("[ERROR] Request error occurred", file=sys.stderr)
        print(f"Details: {req_err}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise

    except Exception as err:
        print("[ERROR] Unexpected error occurred", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise
