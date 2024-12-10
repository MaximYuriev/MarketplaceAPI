from pydantic import BaseModel, Field, ConfigDict


class OuterBalanceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    balance: int


class UpdateBalanceSchema(BaseModel):
    balance: int = Field(default=0, gt=0, validation_alias="addToBalance")
