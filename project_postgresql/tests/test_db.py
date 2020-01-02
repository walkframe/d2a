import pytest
from sqlalchemy import (
    select,
    insert,
    delete,
    update,
    func,
)

@pytest.fixture(scope='function')
def author_model():
    from books.models_sqla import Author
    return Author


@pytest.fixture(scope='function')
def author_table(author_model):
    return author_model.__table__


@pytest.fixture(scope='function')
def author_a():
    from books.models import Author
    return Author.objects.get_or_create(name='a', age=20)[0]


@pytest.fixture(scope='function')
def author_b():
    from books.models import Author
    return Author.objects.get_or_create(name='b', age=15)[0]


@pytest.fixture()
def authors():
    from books.models import Author
    return Author.objects.all().order_by('id')


@pytest.mark.django_db
class Test_query_expression:
    def _callFUT(self, stmt):
        from d2a.db import query_expression
        return query_expression(stmt)

    def test_query_expression(self, author_table, author_a, author_b):
        stmt = select([
            author_table.c.id,
            author_table.c.name,
        ]).select_from(author_table).order_by(author_table.c.age)
        actual = self._callFUT(stmt)
        expected = [
            {'id': author_b.id, 'name': author_b.name},
            {'id': author_a.id, 'name': author_a.name},
        ]
        assert actual == expected


@pytest.mark.django_db
class Test_execute_expression:
    def _callFUT(self, stmt):
        from d2a.db import execute_expression
        return execute_expression(stmt)

    def test_insert_expression(self, author_table, authors):
        expected = [
            {'name': 'a', 'age': 10},
            {'name': 'b', 'age': 20},
            {'name': 'c', 'age': 30},
        ]
        stmt = insert(author_table).values(expected)
        assert self._callFUT(stmt) == 3
        actual = list(authors.values('name', 'age'))
        assert actual == expected

    def test_update_expression(self, author_table, author_a, author_b, authors):
        stmt = update(author_table).where(author_table.c.id == author_a.id).values(
            name=func.UPPER(author_table.c.name),
            age=author_table.c.age + 1,
        )
        assert self._callFUT(stmt) == 1
        actual = list(authors.values('name', 'age'))
        expected = [
            {'name': 'A', 'age': 21},
            {'name': 'b', 'age': 15},
        ]
        assert actual == expected

    def test_delete_expression(self, author_table, author_a, author_b, authors):
        stmt = delete(author_table).where(author_table.c.id == author_a.id)
        assert self._callFUT(stmt) == 1
        actual = list(authors.values('name', 'age'))
        expected = [
            {'name': 'b', 'age': 15},
        ]
        assert actual == expected


@pytest.mark.skip
class Test_make_session:
    def _callFUT(self, **kwargs):
        from d2a.db import make_session
        return make_session(**kwargs)

    def test_make_session(self, author_model):
        with self._callFUT(autocommit=True, autoflush=True) as session:
            author = author_model()
            author.name = 'c'
            author.age = 30
            session.add(author)
            actual = [
                {'name': a.name, 'age': a.age}
                for a in session.query(author_model).all()
            ]
            expected = [
                {'name': 'c', 'age': 30},
            ]
            assert actual == expected
import pytest
from sqlalchemy import (
    select,
    insert,
    delete,
    update,
    func,
)

@pytest.fixture(scope='function')
def author_model():
    from books.models_sqla import Author
    return Author


@pytest.fixture(scope='function')
def author_table(author_model):
    return author_model.__table__


@pytest.fixture(scope='function')
def author_a():
    from books.models import Author
    return Author.objects.get_or_create(name='a', age=20)[0]


@pytest.fixture(scope='function')
def author_b():
    from books.models import Author
    return Author.objects.get_or_create(name='b', age=15)[0]


@pytest.fixture()
def authors():
    from books.models import Author
    return Author.objects.all().order_by('id')


@pytest.mark.django_db
class Test_query_expression:
    def _callFUT(self, stmt):
        from d2a.db import query_expression
        return query_expression(stmt)

    def test_query_expression(self, author_table, author_a, author_b):
        stmt = select([
            author_table.c.id,
            author_table.c.name,
        ]).select_from(author_table).order_by(author_table.c.age)
        actual = self._callFUT(stmt)
        expected = [
            {'id': author_b.id, 'name': author_b.name},
            {'id': author_a.id, 'name': author_a.name},
        ]
        assert actual == expected


@pytest.mark.django_db
class Test_execute_expression:
    def _callFUT(self, stmt):
        from d2a.db import execute_expression
        return execute_expression(stmt)

    def test_insert_expression(self, author_table, authors):
        expected = [
            {'name': 'a', 'age': 10},
            {'name': 'b', 'age': 20},
            {'name': 'c', 'age': 30},
        ]
        stmt = insert(author_table).values(expected)
        assert self._callFUT(stmt) == 3
        actual = list(authors.values('name', 'age'))
        assert actual == expected

    def test_update_expression(self, author_table, author_a, author_b, authors):
        stmt = update(author_table).where(author_table.c.id == author_a.id).values(
            name=func.UPPER(author_table.c.name),
            age=author_table.c.age + 1,
        )
        assert self._callFUT(stmt) == 1
        actual = list(authors.values('name', 'age'))
        expected = [
            {'name': 'A', 'age': 21},
            {'name': 'b', 'age': 15},
        ]
        assert actual == expected

    def test_delete_expression(self, author_table, author_a, author_b, authors):
        stmt = delete(author_table).where(author_table.c.id == author_a.id)
        assert self._callFUT(stmt) == 1
        actual = list(authors.values('name', 'age'))
        expected = [
            {'name': 'b', 'age': 15},
        ]
        assert actual == expected


@pytest.mark.skip
class Test_make_session:
    def _callFUT(self, **kwargs):
        from d2a.db import make_session
        return make_session(**kwargs)

    def test_make_session(self, author_model):
        with self._callFUT(autocommit=True, autoflush=True) as session:
            author = author_model()
            author.name = 'c'
            author.age = 30
            session.add(author)
            actual = [
                {'name': a.name, 'age': a.age}
                for a in session.query(author_model).all()
            ]
            expected = [
                {'name': 'c', 'age': 30},
            ]
            assert actual == expected

