from binascii import unhexlify

import pytest

from shapely import wkb, wkt
from geoalchemy2 import functions
from sqlalchemy import (
    select,
    insert,
)


@pytest.fixture(scope='function')
def srid():
    return 4326


@pytest.fixture(scope='function')
def LakeModel():
    from places.models_sqla import Lake
    return Lake


@pytest.fixture(scope='function')
def LakeTable(LakeModel):
    return LakeModel.__table__


@pytest.fixture(scope='function')
def polygon_biwa():
    return 'POLYGON ((136.178285013544 35.50194537232863, 136.2689222205695 35.33855302068655, 136.007996927631 35.12542349901801, 135.9008802284256 35.00402683524988, 135.8569349159368 35.02202291592027, 135.9338392128034 35.14788454395553, 135.9118665565545 35.17482961681633, 136.0684217323086 35.33631246923886, 136.010743509661 35.42588605444907, 136.181031595574 35.50194537232863, 136.178285013544 35.50194537232863))'


@pytest.fixture(scope='function')
def insert_lake_biwa(srid, LakeTable, polygon_biwa):
    from d2a.db import execute_expression
    stmt = insert(LakeTable).values([{'name': 'Biwa', 'geom': 'SRID={};{}'.format(srid, polygon_biwa)}])
    execute_expression(stmt)


@pytest.fixture(scope='function')
def polygon_hamana():
    return 'POLYGON ((137.5927747594449 34.68270594009567, 137.5241102086773 34.76002540067644, 137.5488294469562 34.80119528194018, 137.5728620397208 34.79499291598717, 137.5536359655109 34.76792258655016, 137.5584424840656 34.75833304827012, 137.5859083043745 34.78653439228995, 137.6106275426533 34.7887900834393, 137.6223005162785 34.80119528194018, 137.6456464635469 34.79330128065563, 137.6030744420686 34.75720479406168, 137.5811017858198 34.71036865119887, 137.6085676061286 34.7143197121764, 137.6126874791691 34.73915063015775, 137.6195539342486 34.73520075578916, 137.631913553388 34.75325578292335, 137.6483930455769 34.76002540067644, 137.6353467809232 34.74197185339279, 137.6326001988932 34.73237930135899, 137.6120008336638 34.70472395096481, 137.6065076696039 34.68101200434809, 137.5927747594449 34.68157665344774, 137.5927747594449 34.68270594009567))'


@pytest.fixture(scope='function')
def insert_lake_hamana(srid, LakeTable, polygon_hamana):
    from d2a.db import execute_expression
    stmt = insert(LakeTable).values([{'name': 'Hamana', 'geom': 'SRID={};{}'.format(srid, polygon_hamana)}])
    execute_expression(stmt)


@pytest.mark.django_db
class Test_geom:
    def _callFUT(self, stmt):
        from d2a.db import query_expression
        return query_expression(stmt)

    def test_polygon(self, srid, LakeTable, polygon_biwa, polygon_hamana, insert_lake_biwa, insert_lake_hamana):
        # Lake Biwa: 670km^2
        # Lake Hamana: 65km^2

        # lake area > 600km^2
        where = functions.ST_Area(functions.ST_Transform(LakeTable.c.geom, 26986)) > 600 * 1000 * 1000
        stmt = select([
            LakeTable.c.geom,
        ]).select_from(LakeTable).order_by(LakeTable.c.id).where(where)
        actual = self._callFUT(stmt)
        assert len(actual) == 1
        polygon = wkb.loads(actual[0]['geom'].tobytes())
        assert str(polygon) == polygon_biwa
