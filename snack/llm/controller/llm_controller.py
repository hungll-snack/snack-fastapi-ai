from fastapi import APIRouter, Request, Depends, Header
from fastapi.responses import JSONResponse
from datetime import datetime
from llm.service.llm_service_impl import LLMServiceImpl
from llm.service.prompt_builder import PromptBuilder
from weather.service.weather_service_impl import WeatherServiceImpl
import requests
import dotenv
import os
from rag.rag_pipeline import run_rag

llmRouter = APIRouter()


def fetch_user_preference(account_id):
    base_url = os.getenv("DJANGO_BASE_URL", "http://localhost:8000")
    url = f"{base_url}/account-prefer/{account_id}"
    print(f"[DEBUG] 요청 URL: {url}")
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

@llmRouter.post("/llm/search")
async def search_llm(
    request: Request,
    usertoken: str = Header(...),
    account_id: str = Header(...),
    llmService: LLMServiceImpl = Depends(LLMServiceImpl),
):
    data = await request.json()
    query = data.get("query")

    if not query or not account_id:
        return JSONResponse(status_code=400, content={"message": "query/account_id 누락"})

    # ✅ Django API 호출로 선호 정보 가져오기
    prefer = fetch_user_preference(account_id)
    if not prefer:
        print(f"[경고] account_id={account_id}의 선호도 정보 없음 — 기본 프롬프트로 진행")
        prefer = {}  # 비어 있는 dict로 처리

    weather = WeatherServiceImpl().get_seoul_weather()

    builder = PromptBuilder(prefer_model=prefer, weather=weather)
    prompt = builder.build_prompt(query)

    answer = llmService.get_response_from_openai(prompt)
    if not answer:
        answer = "응답이 없습니다"

    return JSONResponse(content={
        "response": answer  # ✅ 프론트와 맞춤
    })

