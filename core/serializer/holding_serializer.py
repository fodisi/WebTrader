#!/usr/bin/env python3

from flask_marshmallow import Schema, fields


class HoldingSerializer(Schema):
    """Serializer for model.Holding objects."""
    class Meta:
        fields = (
            'id',
            'username',
            'ticker_symbol',
            'volume',
            'average_price'
        )
