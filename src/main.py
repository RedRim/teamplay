from fastapi import FastAPI

from auth.routers import router as auth_router
# from demo_auth.demo_jwt_schema import router as demo_jwt_auth_router

# auth_router.include_router(demo_jwt_auth_router)
app = FastAPI()
app.include_router(auth_router)