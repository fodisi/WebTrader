#!/usr/bin/env python3

from flask_marshmallow import Schema, fields


class OrderSerializer(Schema):
    class Meta:
        fields = ('id',
                  'username',
                  'ticker_symbol',
                  'datetime',
                  'order_type',
                  'unit_price',
                  'volume',
                  'fee',
                  'cost_proceeds'
                  )
