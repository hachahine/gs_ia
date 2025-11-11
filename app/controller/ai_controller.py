from app.service.ai_service import extract_skills
from app.model.models import SkillsRequest
from fastapi import APIRouter
from fastapi import HTTPException


router = APIRouter()

# health check
@router.get("/")
async def health_check():
    return {"msg": "service is running"}


@router.post("/api/v1/skills")
async def get_skills(request: SkillsRequest):
    try:

        result = extract_skills(request.text, request.api_key)
        return result
    

    except ValueError as e:
        if str(e) == "Invalid API key":
            raise HTTPException(status_code=401, detail="Invalid API key")

        else:
            raise HTTPException(status_code=500, detail=str(e))


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


