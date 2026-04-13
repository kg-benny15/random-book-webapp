from sqlmodel import SQLModel, Field


class ReadingMaterial(SQLModel, table=True):
    __tablename__ = "reading_materials"

    id: int | None = Field(default=None, primary_key=True)
    year: int | None = Field(default=None, gt=1000)
    tittle: str = Field(min_length=1, max_length=50)
    author: str = Field(min_length=1, max_length=30)
    pages: int = Field(gt=1)
    was_finished: bool = Field(default=False)
