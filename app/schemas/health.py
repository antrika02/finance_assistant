from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Response returned by the health endpoint.
    """

    status: str
    database: str
    application: str
    version: str