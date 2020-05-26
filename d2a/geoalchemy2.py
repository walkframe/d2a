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
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.PointField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.LineStringField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.PolygonField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.MultiPointField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.MultiLineStringField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.MultiPolygonField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.GeometryCollectionField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Geography if f.geography else geotypes.Geometry,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'dimension': f.dim,
                'spatial_index': f.spatial_index,
            },
        },
    },
    models.RasterField: {
        '__callback__': lambda f: {
            '__default_type__': geotypes.Raster,
            '__default_type_kwargs__': {
                'geometry_type': f.geom_type,
                'srid': f.srid,
                'spatial_index': f.spatial_index,
            },
        }
    },
}
