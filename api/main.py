import os
import uuid
from typing import List
from fastapi import FastAPI, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware

VERSION: str = '1.0.1'
app = FastAPI(
    title='coding_class_api',
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
@app.get('/versionz')
def versionz():
    return app.version