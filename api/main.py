import os
import uuid
from typing import List
from fastapi import FastAPI, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from api.infrastructure.postgres.dbcontext import DBContext
from api.services.events_router import router as events_router
from api.services.users_router import router as users_router
from api.services.orders_router import router as orders_router
from api.services.executesql_router import router as executesql_router

VERSION: str = '1.0.1'
app = FastAPI(
    title='Group 4 Project API',
    version=VERSION,
    docs_url='/docs',
    redoc_url='/redoc'
)

origins = [
    'http://localhost',
    'http://localhost:8890',
    'http://localhost:8890/',
    'http://0.0.0.0:8890',
    'http://0.0.0.0:8890/'
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_headers=['*'], allow_methods=['*'], expose_headers=['*'])

app.include_router(events_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(executesql_router)

@app.get('/versionz')
def versionz():
    return app.version