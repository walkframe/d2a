import pytest
import sqlalchemy as sa

from d2a.original_types import CIText


def info(table):
    result = {}
    for key, col in table.c.items():
        result[key] = {
            'primary_key': col.primary_key,
            'unique': col.unique,
            'type': type(col.type),
            'nullable': col.nullable,
        }
        if col.default:
            default = col.default.arg
            if callable(default):
                # because it can't check function's equality.
                default = default.__name__
            result[key]['default'] = default
    return result


class TestPostgreSQL(object):
    @pytest.fixture
    def models_sqla(self):
        import models_sqla
        return models_sqla

    def test_CategoryRelation(self, models_sqla):
        actual = info(models_sqla.CategoryRelation.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': False,
            },
            'category1_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': False,
            },
            'category2_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': False,
            },
            'type': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.VARCHAR,
                'nullable': True,
            },
        }
        assert actual == expected

    def test_Author(self, models_sqla):
        actual = info(models_sqla.Author.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': False,
            },
            'name': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.VARCHAR,
                'nullable': False,
            },
            'age': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.SMALLINT,
                'nullable': False,
            },
            'email': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.VARCHAR,
                'nullable': True,
            },
        }
        assert actual == expected

    def test_Category(self, models_sqla):
        actual = info(models_sqla.Category.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': False,
            },
            'name': {
                'primary_key': False,
                'unique': False,
                'type': CIText,
                'nullable': False,
            },
            'created': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.TIMESTAMP,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_Book(self, models_sqla):
        actual = info(models_sqla.Book.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.postgresql.UUID,
                'nullable': False,
                'default': 'uuid4',
            },
            'price': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.JSONB,
                'nullable': False,
            },
            'title': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.VARCHAR,
                'nullable': False,
            },
            'description': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.TEXT,
                'nullable': True,
            },
            'author_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': True,
            },
            'content': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.BYTEA,
                'nullable': False,
            },
            'tags': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.ARRAY,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_BookCategory(self, models_sqla):
        actual = info(models_sqla.BookCategory.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': False,
            },
            'book_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.UUID,
                'nullable': False,
            },
            'category_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INTEGER,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_Sales(self, models_sqla):
        actual = info(models_sqla.Sales.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.postgresql.BIGINT,
                'nullable': False,
            },
            'book_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.UUID,
                'nullable': False,
            },
            'sold': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.TIMESTAMP,
                'nullable': False,
            },
            'reservation': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INTERVAL,
                'nullable': True,
            },
            'source': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INET,
                'nullable': True,
            },
        }
        assert actual == expected
