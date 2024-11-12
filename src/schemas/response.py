from pydantic import BaseModel


class ResponseModel(BaseModel):
    detail: str
    data: list | None = None