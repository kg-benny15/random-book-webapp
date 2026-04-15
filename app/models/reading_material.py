from sqlmodel import SQLModel, Field


class ReadingMaterial(SQLModel, table=True):
    __tablename__ = "reading_materials"

    id: int | None = Field(default=None, primary_key=True)
    year: int | None = Field(default=None, gt=1000)
    tittle: str = Field(min_length=1)
    author: str = Field(min_length=1)
    type: str = Field()
    pages: int = Field(gt=1)
    was_finished: bool = Field(default=False)


class AddReadingMaterial(SQLModel):
    pass


class UpdateReadingMaterial(SQLModel):
    pass


class MaterialResume(SQLModel):
    pass


class ReadingMaterialResponse(SQLModel):
    pass
