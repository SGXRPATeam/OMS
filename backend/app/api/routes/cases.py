from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_case():
    return {"message": "Case created successfully"}


@router.get("/")
def get_all_cases():
    return {"message": "Fetched all cases"}


@router.put("/{case_id}")
def update_case(case_id: str):
    return {"message": f"Case {case_id} updated successfully"}


@router.delete("/{case_id}")
def delete_case(case_id: str):
    return {"message": f"Case {case_id} deleted successfully"}