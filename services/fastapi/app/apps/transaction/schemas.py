from pydantic import BaseModel


class TransactionResponse(BaseModel):
    title: str
    description: str
