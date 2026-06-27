# exercise2_2_file_extension.py
from pydantic import BaseModel, Field, field_validator

# TODO: Create a BaseModel SaveReport with filename and content fields.
# Use @field_validator to validate that the filename ends with either '.txt' or '.md'.
# Raise a ValueError if it doesn't.
class SaveReport(BaseModel):
    pass
