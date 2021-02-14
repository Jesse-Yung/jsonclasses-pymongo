from __future__ import annotations
from typing import ClassVar, TypeVar, Any, Union, Type
from jsonclasses import jsonclass, ORMObject, ObjectNotFoundException
from pymongo.collection import Collection
from pymongo.database import Database
from bson.objectid import ObjectId
from inflection import pluralize
from .utils import default_db
from .encoder import Encoder
from .query import IDQuery, ListQuery, SingleQuery, OptionalSingleQuery


@jsonclass
class BaseMongoObject(ORMObject):
    """BaseMongoObject is a `JSONObject` subclass for defining your business
    models with MongoDB. A `BaseMongoObject` class represents a MongoDB
    collection. This class doesn't define standard primary key field and
    timestamp fields. If you want to use standard fields, consider using
    `MongoObject`.
    """

    _collection: ClassVar[Collection]

    @classmethod
    def db(cls) -> Database:
        return default_db()

    @classmethod
    def collection(cls) -> Collection:
        try:
            return cls._collection
        except AttributeError:
            cls._collection = cls.db().get_collection(
                                    pluralize(cls.__name__).lower())
            return cls._collection

    def _database_write(self: T) -> None:
        Encoder().encode_root(self).execute()

    @classmethod
    def delete_by_id(self, id: str) -> None:
        deletion_result = self.collection().delete_one({'_id': ObjectId(id)})
        if deletion_result.deleted_count < 1:
            raise ObjectNotFoundException(
                f'{self.__name__} with id \'{id}\' is not found.')
        else:
            return None

    @classmethod
    def delete(self, *args, **kwargs) -> int:
        if len(args) == 0:
            args = ({},)
        return self.collection().delete_many(*args, **kwargs).deleted_count

    @classmethod
    def find_by_id(cls: Type[T], id: Union[str, ObjectId]) -> IDQuery:
        return IDQuery(cls=cls, id=id)

    @classmethod
    def with_id(cls: Type[T], id: Union[str, ObjectId]) -> IDQuery:
        return cls.find_by_id(id)

    @classmethod
    def find(cls: Type[T], **kwargs: Any) -> ListQuery:
        return ListQuery(cls=cls, filter=kwargs)

    @classmethod
    def find_one(cls: Type[T], **kwargs: Any) -> SingleQuery:
        if kwargs.get('id'):
            kwargs['_id'] = ObjectId(kwargs['id'])
            del kwargs['id']
        return SingleQuery(ListQuery(cls=cls, filter=kwargs))

    @classmethod
    def find_by(cls: Type[T], **kwargs: Any) -> OptionalSingleQuery:
        return OptionalSingleQuery(cls.find_one(**kwargs))


T = TypeVar('T', bound=BaseMongoObject)
