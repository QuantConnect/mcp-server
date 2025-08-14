import re

path = 'src/models.py'

# Read the file content.
with open(path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Add the extra import (after `from __future__` to avoid errors).
lines.insert(5, 'from pydantic import RootModel, ConfigDict\n')
content = ''.join(lines)

# Perform string replacements.
content = content.replace('__root__', 'RootModel').replace('ResponseModel', 'Response')

# Replace
# ```
#    class Config:
#        extra = Extra.forbid
# ```
# with
# `model_config = ConfigDict(extra='forbid')`
# to avoid warnings when running pytest.
content = content.replace('class Config:', "model_config = ConfigDict(extra='forbid')")\
    .replace('    extra = Extra.forbid', '')

# Fix datetime field schema validation issues
# The problem is that Pydantic generates strict JSON schemas for datetime fields
# that don't match the actual API response format. We need to make datetime fields
# more flexible by using custom field definitions that allow for various datetime formats.

# Import the necessary modules for custom datetime handling
if 'from datetime import datetime as dt_datetime' not in content:
    content = content.replace(
        'from pydantic import BaseModel, Field',
        'from pydantic import BaseModel, Field\nfrom datetime import datetime as dt_datetime'
    )

# Replace datetime field definitions to be more flexible
# The key insight is that we need to allow datetime fields to accept both string and datetime types
# This prevents strict JSON schema validation failures when the API returns datetime strings
# in formats that don't exactly match the JSON Schema "date-time" specification

# Replace Optional[datetime] with Union[str, dt_datetime, None]
content = re.sub(
    r'Optional\[datetime\]',
    'Union[str, dt_datetime, None]',
    content
)

# Replace required datetime fields with Union[str, dt_datetime]
content = re.sub(
    r'(\s+\w+: Annotated\[)datetime(\s*,)',
    r'\1Union[str, dt_datetime]\2',
    content
)

# Save the new file content.
with open(path, 'w', encoding='utf-8') as file:
    file.write(content)
