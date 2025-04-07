from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from weather.service.weather_service_impl import WeatherServiceImpl

weatherRouter = APIRouter()

async def injectWeatherService() -> WeatherServiceImpl:
    return WeatherServiceImpl()

@weatherRouter.get("/weather/seoul")
async def get_weather(
    weatherService: WeatherServiceImpl = Depends(injectWeatherService)
):
    print("controller -> get_weather()")
    result = weatherService.get_seoul_weather()
    return JSONResponse(content=result)
