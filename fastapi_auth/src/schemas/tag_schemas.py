from pydantic import BaseModel, Field


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int = 1
    name: str

    class Config:
        orm_mode = True
