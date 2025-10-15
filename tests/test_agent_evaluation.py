import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

@pytest.mark.asyncio
async def test_weather_agent_zhtw_evaluation():
    """使用評估集測試 weather_agent 的能力。"""
    await AgentEvaluator.evaluate(
        agent_module="weather_agent",
        eval_dataset_file_path_or_dir="weather_agent/weather_evaluation_zhtw.evalset.json",
    )

@pytest.mark.asyncio
async def test_weather_agent_en_evaluation():
    """使用評估集測試 weather_agent_en 的能力。"""
    await AgentEvaluator.evaluate(
        agent_module="weather_agent_en",
        eval_dataset_file_path_or_dir="weather_agent_en/Weather_evaluation.evalset.json",
    )
