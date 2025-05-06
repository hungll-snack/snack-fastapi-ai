from fastapi import APIRouter, Request, Depends, Header
from fastapi.responses import JSONResponse
from datetime import datetime
from llm.service.llm_service_impl import LLMServiceImpl
from llm.service.prompt_builder import PromptBuilder
from weather.service.weather_service_impl import WeatherServiceImpl
import requests
import dotenv
import os

llmRouter = APIRouter()

dotenv.load_dotenv()

DJANGO_BASE_URL = os.getenv("DJANGO_BASE_URL")

def fetch_user_preference(account_id):
    url = f"{DJANGO_BASE_URL}/account-prefer/{account_id}"
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
        return JSONResponse(status_code=404, content={"message": "선호 정보 없음"})

    weather = WeatherServiceImpl().get_seoul_weather()

    # ✅ JSON 선호 데이터를 PromptBuilder가 인식할 수 있도록 가공 필요
    builder = PromptBuilder(prefer_model=prefer, weather=weather)
    prompt = builder.build_prompt(query)

    answer = llmService.get_response_from_openai(prompt)

    return JSONResponse(content={"response": answer})
