from pydantic import BaseModel


class ErrorDetail(BaseModel):
    msg: str


class Unauthorized(BaseModel):
    detail: ErrorDetail


class Forbidden(BaseModel):
    detail: ErrorDetail


class NotFound(BaseModel):
    detail: ErrorDetail
