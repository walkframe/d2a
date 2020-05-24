# coding: utf-8
from django.contrib.gis.db import models
from geoalchemy2 import types as geotypes

"""
Mapping definition

:geoalchemy2:

  - https://github.com/django/django/blob/master/django/contrib/gis/db/models/fields.py
  - https://github.com/geoalchemy/geoalchemy2/blob/master/geoalchemy2/types.py

"""

geo_mapping = {
    models.GeometryField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.PointField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.LineStringField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.PolygonField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.MultiPointField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.MultiLineStringField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.MultiPolygonField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.GeometryCollectionField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Geography if f.geography else geotypes.Geometry,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.RasterField: {
        '_callback': lambda f: {
            '_default_type': geotypes.Raster,
            '_default_type_option': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'spatial_index': f.spatial_index,
            },
        }
    },
}
