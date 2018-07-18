#!/usr/bin/env python3

from enum import IntEnum, unique


@unique
class OrderType(IntEnum):
    """Specifies the different types of orders implemented available."""
    NONE = -1
    MARKET_BUY = 0
    MARKET_SELL = 1
    OTC_BUY = 2
    OTC_SELL = 3
