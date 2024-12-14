from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute, Session

T = TypeVar("T")


class BaseDAO(Generic[T]):
    """Fluent interface wrapper above simple SQLAlchemy queries
    Examples:
        objs = repo.select('id').where(name='test').order_by('id', 'desc').all()

        objs = repo.select(id='id_label').where_in(id=[1, 2]).limit(5).all()

        objs = repo.where(id=230423).all()
    """

    model: type[T] | None = None

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.field_name_to_orm_field = self.__build_fields_mapping()

    def __build_fields_mapping(self) -> dict[str, InstrumentedAttribute[Any]]:
        """Returns map field_name -> sqlalchemy orm field"""
        field_name_to_orm_field = {
            attr: self.model.__dict__[attr]
            for attr, value in self.model.__dict__.items()
            if isinstance(value, InstrumentedAttribute)
        }

        return field_name_to_orm_field

    def _get_field(self, name: str) -> InstrumentedAttribute[Any]:
        return self.field_name_to_orm_field[name]

    def one_or_none(self, value: Any, field: str = "id") -> T | None:
        id_field = self._get_field(field)
        stmt = select(self.model).where(id_field == value)  # type: ignore[arg-type]
        return self.db_session.execute(stmt).scalars().one_or_none()

    def create(self, data: dict[str, Any] | BaseModel) -> T:
        if isinstance(data, BaseModel):
            data = data.model_dump()

        db_obj = self.model(**data)  # type: ignore[misc]
        self.db_session.add(db_obj)
        return db_obj

    def commit(self) -> None:
        self.db_session.commit()
