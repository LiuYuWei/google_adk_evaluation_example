import asyncio
import sys
import os
import argparse
import pandas as pd
from google.adk.evaluation import AgentEvaluator
from google.adk.evaluation.eval_set import EvalSet
from google.adk.evaluation.eval_config import (
    get_evaluation_criteria_or_default,
    get_eval_metrics_from_config,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="使用 ADK Python SDK 執行評估並輸出所有結果到 CSV。"
    )

    parser.add_argument(
        "--config",
        default="./weather_agent/test_config.json",
        help="評估設定檔路徑（對應 --config_file_path）。",
    )
    parser.add_argument(
        "--evalset",
        default="weather_agent/weather_evaluation_zhtw.evalset.json",
        help="評估資料集 EvalSet JSON 路徑。",
    )
    parser.add_argument(
        "--module-name",
        default="weather_agent",
        help="要載入的 Agent 模組名稱（與 adk eval 的第一個參數相同）。",
    )
    parser.add_argument(
        "--num-runs",
        type=int,
        default=1,
        help="每個評估案例的執行次數（預設 1）。",
    )
    parser.add_argument(
        "--output",
        default="evaluation_all_metrics.csv",
        help="輸出 CSV 檔案名稱。",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8-sig",
        help="輸出編碼（預設 utf-8-sig，方便 Excel 開啟）。",
    )
    parser.add_argument(
        "--print-detailed-results",
        action="store_true",
        help="是否輸出詳細結果（模擬 adk eval 的 --print_detailed_results）。",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="顯示詳細執行訊息。",
    )
    return parser.parse_args()


async def run_evaluation(
    config_path: str,
    evalset_path: str,
    module_name: str,
    num_runs: int,
    output_filename: str,
    encoding: str,
    print_detailed_results: bool,
    verbose: bool,
):
    # 1. 載入設定與資料集
    if verbose:
        print(f"[INFO] Loading eval config: {config_path}")
    eval_config = get_evaluation_criteria_or_default(config_path)

    if verbose:
        print(f"[INFO] Loading eval set: {evalset_path}")
    with open(evalset_path, "r", encoding="utf-8") as f:
        eval_set = EvalSet.model_validate_json(f.read())

    # 2. 載入 Agent 與 Metrics
    if verbose:
        print(f"[INFO] Loading module: {module_name}")
    agent_for_eval = AgentEvaluator._get_agent_for_eval(module_name=module_name)
    eval_metrics = get_eval_metrics_from_config(eval_config)

    # 3. 執行評估
    print("Running evaluation...")
    eval_results_by_eval_id = await AgentEvaluator._get_eval_results_by_eval_id(
        agent_for_eval=agent_for_eval,
        eval_set=eval_set,
        eval_metrics=eval_metrics,
        num_runs=num_runs,
    )
    print("Evaluation complete.")

    # 4. 處理結果
    all_results_for_csv = []
    for eval_id, eval_case_results in eval_results_by_eval_id.items():
        for case_result in eval_case_results:
            for invocation_result in case_result.eval_metric_result_per_invocation:
                base_row = {
                    "eval_id": eval_id,
                    "prompt": AgentEvaluator._convert_content_to_text(
                        invocation_result.expected_invocation.user_content
                    ),
                    "expected_response": AgentEvaluator._convert_content_to_text(
                        invocation_result.expected_invocation.final_response
                    ),
                    "actual_response": AgentEvaluator._convert_content_to_text(
                        invocation_result.actual_invocation.final_response
                    ),
                    "expected_tool_calls": AgentEvaluator._convert_tool_calls_to_text(
                        invocation_result.expected_invocation.intermediate_data
                    ),
                    "actual_tool_calls": AgentEvaluator._convert_tool_calls_to_text(
                        invocation_result.actual_invocation.intermediate_data
                    ),
                }

                for metric_result in invocation_result.eval_metric_results:
                    metric_name = metric_result.metric_name
                    base_row[f"{metric_name}_score"] = metric_result.score
                    base_row[f"{metric_name}_status"] = str(
                        metric_result.eval_status
                    )
                    base_row[f"{metric_name}_threshold"] = metric_result.threshold

                all_results_for_csv.append(base_row)

                # 額外輸出詳細結果
                if print_detailed_results:
                    print(
                        f"\n--- Eval ID: {eval_id} ---\n"
                        f"Prompt:\n{base_row['prompt']}\n"
                        f"Expected:\n{base_row['expected_response']}\n"
                        f"Actual:\n{base_row['actual_response']}\n"
                    )

    # 5. 寫出 CSV
    if all_results_for_csv:
        df = pd.DataFrame(all_results_for_csv)
        df.to_csv(output_filename, index=False, encoding=encoding)
        print(f"Saved all evaluation results to {output_filename}")
    else:
        print("No evaluation results to save.")


async def main():
    args = parse_args()
    await run_evaluation(
        config_path=args.config,
        evalset_path=args.evalset,
        module_name=args.module_name,
        num_runs=args.num_runs,
        output_filename=args.output,
        encoding=args.encoding,
        print_detailed_results=args.print_detailed_results,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    asyncio.run(main())
