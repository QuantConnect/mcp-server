import os
import pytest
from types import UnionType
import jsonschema
from json import loads
from pydantic import ValidationError, TypeAdapter
from datetime import datetime

_RUN_QUANTCONNECT_API_TESTS = os.getenv("RUN_QUANTCONNECT_API_TESTS") == "1"


def _require_quantconnect_api_tests() -> None:
    if not _RUN_QUANTCONNECT_API_TESTS:
        pytest.skip(
            "QuantConnect integration tests disabled. "
            "Set RUN_QUANTCONNECT_API_TESTS=1 to enable network-backed tests."
        )

async def validate_response(
        mcp, tool_name, structured_response, output_class):
    # Check if the response schema is valid JSON.
    jsonschema.validate(
        instance=structured_response, 
        schema=mcp._tool_manager.get_tool(tool_name).fn_metadata.output_schema
    )

    # Create and return the output model.
    if isinstance(output_class, UnionType):
        structured_response = structured_response['result']
    return TypeAdapter(output_class).validate_python(structured_response)

async def validate_models(
        mcp, tool_name, input_args={}, output_class=None, 
        success_expected=True):
    _require_quantconnect_api_tests()
    # Call the tool with the arguments. If the input args are invalid,
    # it raises an error.
    unstructured_response, structured_response = await mcp.call_tool(
        tool_name, {'model': input_args}
    )
    # Check if the response has the success flag.
    assert loads(
        unstructured_response[0].text
    ).get('success', True) == success_expected, structured_response
    if not success_expected:
        return structured_response
    # Check if the response respects the output_class.
    output_model = await validate_response(
        mcp, tool_name, structured_response, output_class
    )
    # Return an instance of the output_class.
    return output_model

async def ensure_request_fails(mcp, tool_name, input_args={}):
    # The input_args should be valid for the Pydantic model conversion,
    # but should be invalid for the API.
    structured_response = await validate_models(
        mcp, tool_name, input_args, success_expected=False
    )
    return structured_response

async def ensure_request_raises_validation_error(tool_name, class_, args):
    with pytest.raises(ValidationError) as error:
        class_.model_validate(args)
    assert error.type is ValidationError

async def ensure_request_raises_validation_error_when_omitting_an_arg(
        tool_name, class_, minimal_payload):
    # This test ensures that if we omit one of the arguments from the
    # `minimal_payload`, the payload doesn't respect the required 
    # properties of the Pydantic model (`class_`). If the YAML is 
    # updated so that the required properties of the model are 
    # adjusted, this test will fail and we'll be informed of the 
    # change.
    class_.model_validate(minimal_payload)
    for key in minimal_payload:
        await ensure_request_raises_validation_error(
            tool_name, class_, 
            {k: v for k, v in minimal_payload.items() if k != key}
        )

async def ensure_request_fails_when_including_an_invalid_arg(
        mcp, tool_name, minimal_payload, invalid_arguments):
    # Try to send the request with an invalid argument.
    for arg in invalid_arguments:
        await ensure_request_fails(mcp, tool_name, minimal_payload | arg)

def create_timestamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')
