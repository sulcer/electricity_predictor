from .health import router as health_router
from .prediction import router as prediction_router
from .price import router as price_router
from .production import router as production_router

__all__ = [health_router, prediction_router, price_router, production_router]
