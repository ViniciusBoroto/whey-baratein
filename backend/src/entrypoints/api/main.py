from fastapi import FastAPI
from entrypoints.api.middleware.exception_handler import register_exception_handlers
from entrypoints.api.middleware.cors import setup_cors
from entrypoints.api.routes import users, whey, brands, auth

def create_app() -> FastAPI:
    app = FastAPI(title="Whey Baratein API", version="1.0.0")
    
    setup_cors(app)
    register_exception_handlers(app)
    
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(whey.router, prefix="/api/v1/whey", tags=["whey"])
    app.include_router(brands.router, prefix="/api/v1/brands", tags=["brands"])
    
    return app

app = create_app()
