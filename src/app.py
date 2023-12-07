from fastapi import FastAPI
from src.core.auth.api import auth_router
from src.users.api import users_router

app = FastAPI(debug=True)
app.include_router(auth_router)
app.include_router(users_router)
