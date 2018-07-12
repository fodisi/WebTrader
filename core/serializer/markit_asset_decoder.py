#!/usr/bin/env python3


import json


class MarkitOnDemmandAssetDecoder(json.JSONDecoder):
    """Decodes a MarkitOnDemmand JSON object to an Asset-compatible dictionary."""

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.convert, *args, **kwargs)

    def convert(self, obj):
        """Converts a MarkitOnDemmand JSON object to a dictionary compatible with model.Asset.

        Args:
            - obj: MarkitOnDemmand JSON object

        Returns:
            (dictionary) a dictionary compatible with model.Asset.

        """

        if isinstance(obj, dict):
            try:
                return {
                    'name': obj['Name'],
                    'symbol': obj['Symbol'],
                    'exchange': obj['Exchange']
                }
            except KeyError as k:
                msg = 'Invalid JSON object. Expected attributes not in place.\nDetails: {0}'
                raise ValueError(msg.format(k.args[0]))
            except Exception:
                raise
        else:
            raise TypeError('Invalid object type.')
