#!/usr/bin/env python3

from flask_marshmallow import Schema, fields


class OrderSerializer(Schema):
    """Serializer for model.Order objects."""
    class Meta:
        fields = (
            'id',
            'username',
            'ticker_symbol',
            'date_time',
            'order_type',
            'unit_price',
            'volume',
            'fee',
            'cost_proceeds'
        )
