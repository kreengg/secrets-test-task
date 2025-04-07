from pydantic import BaseModel


class ErrorResponse(BaseModel):
    status_code: int
    detail: str


class StatusResponse(BaseModel):
    status: str
