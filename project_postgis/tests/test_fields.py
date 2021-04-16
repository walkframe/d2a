import pytest
import sqlalchemy as sa


class TestGeoAlchemyFieldType(object):
    @pytest.fixture
    def LakeTable(self):
        from models_sqla import Lake
        return Lake.__table__

    @pytest.fixture
    def AddressTable(self):
        from models_sqla import Address
        return Address.__table__

    def test_LakeTable(self, LakeTable):
        actual = {
            'geometry_type': LakeTable.c.geom.type.geometry_type, 
            'srid': LakeTable.c.geom.type.srid,
        }
        expected = {
            'geometry_type': 'POLYGON', 
            'srid': 4326,
        }
        assert actual == expected

    def test_AddressTable(self, AddressTable):
        actual = {
            'geometry_type': AddressTable.c.geom.type.geometry_type, 
            'srid': AddressTable.c.geom.type.srid,
        }
        expected = {
            'geometry_type': 'POINT', 
            'srid': 4326,
        }
        assert actual == expected

