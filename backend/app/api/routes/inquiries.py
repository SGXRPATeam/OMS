from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def create_inquiry():
    return {"message": "Inquiry created successfully"}


@router.get("/")
def get_all_inquiries():
    return {"message": "Fetched all inquiries"}


@router.put("/{inquiry_id}")
def update_inquiry(inquiry_id: str):
    return {"message": f"Inquiry {inquiry_id} updated successfully"}


@router.delete("/{inquiry_id}")
def delete_inquiry(inquiry_id: str):
    return {"message": f"Inquiry {inquiry_id} deleted successfully"}