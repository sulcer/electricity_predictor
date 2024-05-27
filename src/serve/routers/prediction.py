from fastapi import APIRouter

router = APIRouter(
    tags=["predict"],
    prefix="/predict"
)


@router.get("/")
def predict():
    return {"message": "returns prediction"}
