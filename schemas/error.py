from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """
    Defines the structure of an error message response.
    """
    message: str
