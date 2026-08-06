from fastapi import APIRouter, HTTPException
from backend.models.schemas import ConvertRequest, ConvertResponse
from backend.services.tone_converter import convert_tone

router = APIRouter()

@router.post("/convert", response_model=ConvertResponse)
async def convert_text_endpoint(request: ConvertRequest):
    try:
        # 톤 변환 서비스 호출
        converted_result = convert_tone(request.text, request.target_audience)
        return ConvertResponse(
            converted_text=converted_result,
            target_audience=request.target_audience,
            original_text=request.text
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # 내부 오류 로깅 및 500 응답 반환
        print(f"[Error] Tone conversion failed: {str(e)}")
        raise HTTPException(status_code=500, detail="LLM API 호출 중 오류가 발생했습니다.")
