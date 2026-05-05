from fastapi import APIRouter, Depends

from dependencies import get_db_conn
from schemas import CompanyCreate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyResponse)
async def create_company(body: CompanyCreate, conn=Depends(get_db_conn)):
    row = await conn.fetchrow(
        "INSERT INTO companies (name) VALUES ($1) RETURNING *", body.name
    )
    return dict(row)


@router.get("/", response_model=CompanyResponse)
async def get_company(id: int, conn=Depends(get_db_conn)):
    row = await conn.fetchrow("SELECT * FROM companies where id = $1", id)
    return dict(row)
