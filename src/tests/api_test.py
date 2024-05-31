from src.data.fetch import Fetcher


def test_weather_api():
    fetcher = Fetcher()
    response = fetcher.ping_weather_api()
    assert len(response) > 0


def test_price_api():
    fetcher = Fetcher()
    response = fetcher.ping_price_api()
    assert len(response) > 0


def test_production_api():
    fetcher = Fetcher()
    response = fetcher.ping_production_api()
    assert len(response) > 0
