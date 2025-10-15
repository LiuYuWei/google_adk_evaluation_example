from google.adk.agents.llm_agent import Agent
import random

def query_weather(city_name: str) -> str:
    weather_list = ['陰天']
    weather = random.choice(weather_list)
    return f"{city_name} 的天氣是：{weather}。"

root_agent = Agent(
    model='gemini-2.5-flash',
    name='weather_agent',
    description='weather agent',
    instruction="""
    你是一個天氣預報助理，請根據使用者提供的中文城市名稱，中文回覆該城市的天氣狀況。
    """,
    tools=[query_weather],
)
