#!usr/bin/env python3


from ..wrapper.markit_wrapper import MarkitOnDemand


class Asset():
    """Represents an asset (stock, currency, etc.) traded in an exchange.

    Attributes:
        name (str): name of the asset. May represent the company name, currency name, etc.
        symbol (str): ticker symbol used to uniquely identify the asset.
        exchange (str): name of the exchange where the asset is traded.

    """

    def __init__(self,
                 name='',
                 symbol='',
                 exchange=''):
        """Class constructor. Initializes attributes with specified or default values.

        Args:
            name (str): name of the asset.
            symbol (str): ticker symbol used to uniquely identify the asset.
            exchange (str): name of the exchange where the asset is traded.

        """

        self.name = name
        self.symbol = symbol
        self.exchange = exchange

    @staticmethod
    def search_market_assets(search_input):
        """Searches the market data for a list of assets based on a specific 'search_input'.

        Args:
            search_input (str): The input used to search for assets. Commonly a company name (or partial name) or ticker symbol.

        Returns:
            Asset[]: a list of Asset object attributes updated with market values based on 'search_input'.
            None: if no assets were found based on 'search_input'.

        """
        try:
            result = MarkitOnDemand.lookup(search_input)
        except ValueError:
            # ValueError is expected when calling MarkitOnDemand.lookup.
            # In such cases, just raises the error to be handled by an upper layer.
            raise
        else:
            # MarkitOnDemand.lookup may return None if nothing is found for search_input.
            if result is None:
                return None

            # Creates and returns a lists of assets found.
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
        return MarkitOnDemand.lookup_exchange(ticker_symbol)
