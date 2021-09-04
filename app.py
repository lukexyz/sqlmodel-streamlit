from typing import Optional

from sqlmodel import Field, SQLModel

class Hero(SQLModel, table=True):
    id