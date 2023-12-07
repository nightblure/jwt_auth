from typing import Any

from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, InstrumentedAttribute, Query


class BaseSqlRepository:
    """
    Fluent interface wrapper above simple SQLAlchemy queries
    Examples:
        objs = repo.select('id').where(name='test').order_by('id', 'desc').all()

        objs = repo.select(id='id_label').where_in(id=[1, 2]).limit(5).all()

        objs = repo.where(id=230423).all()
    """
    model = None

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.field_name_to_orm_field = self.__build_fields_mapping()
        self.q = db_session.query(self.model)

    def __build_fields_mapping(self) -> dict[str, InstrumentedAttribute]:
        """Returns map field_name -> sqlalchemy orm field"""
        field_name_to_orm_field = {
            attr: self.model.__dict__[attr]
            for attr, value in self.model.__dict__.items()
            if isinstance(value, InstrumentedAttribute)
        }

        return field_name_to_orm_field

    def _get_field(self, name: str):
        return self.field_name_to_orm_field[name]

    def order_by(self, field: str, order: str = 'asc'):
        orm_field = self._get_field(field)
        self.q = self.q.order_by(orm_field)

        if order == 'desc':
            self.q = self.q.order_by(orm_field.desc())

        return self

    def where(self, **filter_args):
        self.q = self.q.filter_by(**filter_args)
        return self

    def where_in(self, **filter_args):
        """
        :param filter_args: must be dict[str, list | tuple | set]
        """
        filters = [
            self._get_field(field).in_(value)
            for field, value in filter_args.items()
        ]
        self.q = self.q.filter(*filters)
        return self

    def select(self, *fields, **field_to_label):
        """Using examples in class comment"""
        orm_fields = []

        if fields:
            orm_fields = [self._get_field(field) for field in fields]

        if field_to_label:
            orm_fields = [
                self._get_field(field).label(label)
                for field, label in field_to_label.items()
            ]

        if orm_fields:
            self.q = self.db_session.query(*orm_fields)

        return self

    def limit(self, limit: int):
        self.q = self.q.limit(limit)
        return self

    def all(self):
        return self.q.all()

    def where_by_condition(self, field: str, operator: str, value):
        """
        :param field: field name
        :param operator: must be '<', '<=', '>' or '>='
        """
        orm_field = self._get_field(field)

        if operator == '>':
            self.q = self.q.filter(orm_field > value)

        if operator == '>=':
            self.q = self.q.filter(orm_field >= value)

        if operator == '<':
            self.q = self.q.filter(orm_field < value)

        if operator == '<=':
            self.q = self.q.filter(orm_field <= value)

        return self

    def where_null(self, field: str):
        orm_field = self._get_field(field)
        self.q = self.q.filter(orm_field.is_(None))
        return self

    def where_not_null(self, field: str):
        orm_field = self._get_field(field)
        self.q = self.q.filter(orm_field.isnot(None))
        return self

    @property
    def query(self) -> Query:
        return self.q

    def one_or_none(self, value, field: str = 'id'):
        id_field = self._get_field(field)
        return self.q.filter(id_field == value).one_or_none()

    def create(self, data: dict[str, Any] | BaseModel, commit=True):
        data_dict: dict[str, Any] = data

        if isinstance(data, BaseModel):
            data_dict = data.dict()

        db_obj = self.model(**data_dict)

        try:
            self.db_session.add(db_obj)
            if commit:
                self.db_session.commit()

            return db_obj
        except IntegrityError as e:
            self.db_session.rollback()
            raise e

    def update(self, *, id, id_field_name: str = 'id', data: dict[str, Any] | BaseModel, commit=True):
        data_dict: dict[str, Any] = data

        if isinstance(data, BaseModel):
            data_dict = data.dict(exclude_unset=True)

        try:

            id_field = self._get_field(id_field_name)
            q = update(self.model).where(id_field == id).values(**data_dict)
            self.db_session.execute(q)

            if commit:
                self.db_session.commit()

        except IntegrityError as e:
            self.db_session.rollback()
            raise e

    def update_by_object(self, *, db_obj, data: dict[str, Any] | BaseModel, commit=True):

        data_dict: dict[str, Any] = data

        if isinstance(data, BaseModel):
            data_dict = data.dict(exclude_unset=True)

        try:

            for field in self.field_name_to_orm_field:
                if field in data_dict:
                    setattr(db_obj, field, data_dict[field])

            if commit:
                self.db_session.commit()

        except IntegrityError as e:
            self.db_session.rollback()
            raise e

    def delete(self, *, id, id_field_name: str = 'id', commit=True, synchronize_session=False):
        db_obj = self.one_or_none(id=id, id_field_name=id_field_name)
        try:
            db_obj.delete(synchronize_session=synchronize_session)
            if commit:
                self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            raise e
