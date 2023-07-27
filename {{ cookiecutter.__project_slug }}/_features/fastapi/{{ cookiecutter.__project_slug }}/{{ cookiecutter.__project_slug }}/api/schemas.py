"""Entity schemas for the API."""
from pydantic import BaseModel as BaseSchema


class SomeSchema(BaseSchema):
    """Schema for /something endpoint."""
