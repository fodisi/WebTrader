#!/usr/bin/env python3

from flask_marshmallow import Schema, fields


class AssetSerializer(Schema):
    class Meta:
        fields = ('name',
                  'symbol',
                  'exchange'
                  )
