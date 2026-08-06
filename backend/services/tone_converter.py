import os
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.prompts.templates import SYSTEM_PROMPTS

# .env 파일 로드
load_dotenv()

# API 키 및 모델 초기화
api_key = os.getenv("UPSTAGE_API_KEY")
if not api_key:
    raise ValueError("UPSTAGE_API_KEY가 .env 파일에 설정되어 있지 않습니다.")

llm = ChatUpstage(model="solar-pro3", upstage_api_key=api_key)

def convert_tone(text: str, target_audience: str) -> str:
    """
    입력된 텍스트의 어조를 대상(target_audience)에 맞게 변환합니다.
    """
    system_prompt = SYSTEM_PROMPTS.get(target_audience)
    if not system_prompt:
        raise ValueError(f"유효하지 않은 수신 대상입니다: {target_audience}")

    # 프롬프트 템플릿 정의
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "다음 원문을 목적에 맞는 어조로 변환해 주세요:\n\n{text}")
    ])

    # 체인 구성 및 호출
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"text": text})
    
    return result.strip()
