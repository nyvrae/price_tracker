from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
async def register_user():
    pass

@router.post("/login")
async def login_for_access_token():
    pass

@router.get("/me")
async def read_users_me():
    pass