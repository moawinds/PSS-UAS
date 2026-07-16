from ninja import NinjaAPI
from ninja_simple_jwt.auth.views.api import mobile_auth_router

from .routes import router

api = NinjaAPI(
    title="Simple LMS API",
    version="1.0.0",
    description="REST API untuk Simple LMS"
)

# Endpoint API
api.add_router("/", router)

# Endpoint Authentication JWT
api.add_router("/auth/", mobile_auth_router)