from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.routers import router as auth_router
from cyber.routers import router as cyber_router
from notifications.routers import router as notifications_router
# from demo_auth.demo_jwt_schema import router as demo_jwt_auth_router

# auth_router.include_router(demo_jwt_auth_router)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или укажите конкретные источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(cyber_router)
app.include_router(notifications_router)