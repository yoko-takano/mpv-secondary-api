import yfinance as yf


class YahooFinanceService:
    @staticmethod
    def get_exchange_rate(pair: str):
        """
        Fetches the current exchange rate for a given currency pair from Yahoo Finance.
        Example: 'USDBRL=X' for USD to BRL.
        """
        try:
            # Busca a taxa de câmbio no Yahoo Finance
            currency_data = yf.Ticker(pair)
            exchange_rate = currency_data.history(period="1d")['Close'].iloc[0]

            return exchange_rate
        except Exception as e:
            raise Exception(f"Error fetching exchange rate: {str(e)}")
