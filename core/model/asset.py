#!usr/bin/env python3


from ..wrapper.markit_wrapper import MarkitOnDemmand


class Asset():
    """Represents an asset (stock, currency, etc.) traded in an exchange."""

    def __init__(self):
        """Class constructor."""

        self.name = ''
        self.symbol = ''
        self.exchange = ''

    @classmethod
    def assets_from_market_data(cls, search_input):
        """Searches the market data for a list of assets based on a specific 'search_input'.

        Args:
            search_input (str): The input used to search for assets. Commonly a company name (or partial name) or ticker symbol.

        Returns:
            Asset[]: a list of Asset object attributes updated with market values based on 'search_input'.
            None: if no assets were found based on 'search_input'.

        """
        try:
            result = MarkitOnDemmand.lookup(search_input)
        except ValueError:
            raise
        else:
            asset_list = None
            if result is not None:
                asset_list = []
                for item in result:
                    asset = Asset()
                    asset.__dict__.update(item)
                    asset_list.append(asset)

            return asset_list

    @staticmethod
    def get_exchange_name(ticker_symbol):
        """Gets the exchange where 'ticker_symbol' is traded.

        Args:
            ticker_symbol (str): used to identify the exchange where the 'ticker_symbol' is traded.

        Returns:
            None: if no exchange was found based on 'ticker_symbol'. Otherwise;
            string: the name of the exchange where 'ticker_symbol' is traded.
                If 'ticker_symbol' is traded in more than one exchange,
                returns the first exchange found.

        Raises:
            ValueError: if an error message is returned from the API.

        """
        return MarkitOnDemmand.lookup_exchange(ticker_symbol)
