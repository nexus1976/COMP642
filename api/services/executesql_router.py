import uuid
import os
from typing import List, Dict
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from api.infrastructure.postgres.dbcontext import DBContext
from sqlalchemy.orm import Session
from sqlalchemy import * # type: ignore
from api.models.executesql_apimodel import ExecuteSQLModel

router = APIRouter(tags=["executesql"])

def getdata(dbcontext: DBContext, sql: str):
    query = text(sql)
    with dbcontext.engine.connect() as conn:
        result = conn.execute(query)
        return [dict(row) for row in result.mappings()]


@router.post("/executesql", status_code=status.HTTP_200_OK | status.HTTP_500_INTERNAL_SERVER_ERROR)
async def executesql(res: Response, sqlModel: ExecuteSQLModel) -> JSONResponse:
    dbcontext: DBContext = DBContext(host=os.environ['DB_HOST'], dbname=os.environ['DB_NAME'], username=os.environ['DB_UID'], password=os.environ['DB_PWD'])
    data = getdata(dbcontext, sqlModel.sql)
    response = JSONResponse(content=jsonable_encoder(data), status_code=200)
    res.status_code = status.HTTP_200_OK
    return response
    
