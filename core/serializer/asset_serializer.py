#!/usr/bin/env python3

from flask_marshmallow import Schema, fields


class AssetSerializer(Schema):
    """Serializer for model.Asset objects."""
    class Meta:
        fields = (
            'name',
            'symbol',
            'exchange'
        )
