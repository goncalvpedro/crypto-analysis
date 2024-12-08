import ccxt
import pandas as pd
from datetime import datetime

def fetch_historical_data(exchange_id, symbol, timeframe, since=None, limit=100):
    try:
        # Inicializar a exchange
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({'enableRateLimit': True})

        # Verificar se o par de negociação é suportado
        if symbol not in exchange.load_markets():
            raise ValueError(f"O par {symbol} não é suportado pela exchange {exchange_id}")

        # Obter os dados de candles (OHLCV)
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)

        # Converter os dados para um DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        return df

    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return None

wallet = [
    'BTC', 'ETH', 'SOL', 'BNB', 'DOGE', 'LINK', 
    'APT', 'FLOKI', 'SHIB', 'WIF', 'PEPE'
]

if __name__ == "__main__":
    exchange_id = 'binance'  # Nome da exchange
    timeframe = '1d'  # Intervalo de tempo
    since = int(datetime(2020, 1, 1).timestamp() * 1000)  # Data de início (opcional)

    for item in wallet:
        symbol = item + '/USDT'  # Par de negociação

        data = fetch_historical_data(exchange_id, symbol, timeframe, since)

        if data is not None:
            print(data.head())
            # Salvar os dados em um arquivo CSV
            data.to_csv(f'data/{item}.csv', index=False)
            print(f"Dados salvos em 'data/{item}.csv'")
