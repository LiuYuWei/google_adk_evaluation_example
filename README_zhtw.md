# Google ADK 評估範例 (Google ADK Evaluation Example)

這是一個範例專案，旨在展示如何使用 Google Agent Development Kit (ADK) 來建構、測試及評估 AI 智慧體 (Agent)。

專案內包含一個簡單的「天氣智慧體」，它能根據使用者輸入的城市名稱回報天氣狀況。此專案的主要目的是示範 ADK 強大的評估功能，並提供一個清晰的專案結構參考。

此專案包含兩種不同語言版本的智慧體：
1.  `weather_agent/` - 繁體中文版本
2.  `weather_agent_en/` - 英文版本

---

## 專案結構

```
/
├── weather_agent/                  # 繁體中文天氣智慧體
│   ├── agent.py                    # 智慧體的核心邏輯 (指令、工具)
│   ├── weather_evaluation_zhtw.evalset.json  # 繁體中文評估測試集
│   └── .adk/
│       └── eval_history/           # 歷次評估結果的存放處
│
├── weather_agent_en/               # 英文天氣智慧體
│   ├── agent.py                    # 智慧體的核心邏輯 (英文版)
│   └── Weather_evaluation.evalset.json # 英文評估測試集
│
├── .gitignore
├── LICENSE
└── README.md                       # 本說明檔案
```

-   **`agent.py`**: 定義了智慧體的行為，包括它的核心指令 (instruction) 以及可使用的工具 (tools)，例如 `query_weather` 函式。
-   **`*.evalset.json`**: 評估測試集檔案。它包含了一系列的測試案例 (eval_cases)，每個案例都有一個使用者輸入以及預期的理想回覆。ADK 會使用這個檔案來自動化地測試智慧體的表現。
-   **`.adk/eval_history/`**: ADK 自動產生的目錄。每當您執行一次評估，詳細的結果報告 (JSON 格式) 都會儲存在這裡，方便追蹤與分析。

---

## 主要功能

-   使用 `google-adk` 打造的簡易天氣查詢智慧體。
-   示範如何為智慧體定義明確的指令 (instruction) 與工具 (tool)。
-   提供結構化的評估集 (`.evalset.json`)，實現自動化測試與效能評估。
-   包含多語言範例 (英文與繁體中文)，展示了 ADK 在國際化應用上的潛力。
-   提供了一個標準的 ADK 智慧體專案結構，可作為您未來開發的起點。

---

## 如何使用

### 前置需求

1.  **Python**: 建議使用 Python 3.11 或更新版本。
2.  **安裝 Google ADK**:
    ```bash
    pip install google-adk
    ```

### 執行評估

本專案的核心是展示評估流程。您可以使用 `adk eval` 命令來自動化地測試智慧體的表現。

-   **評估繁體中文智慧體**:

    執行以下命令，ADK 將會讀取 `weather_evaluation_zhtw.evalset.json` 中的所有測試案例，並逐一測試 `weather_agent` 的反應。

    ```bash
    adk eval weather_agent/ weather_agent/weather_evaluation_zhtw.evalset.json --config_file_path=./weather_agent/test_config.json --print_detailed_results 
    ```

-   **評估英文智慧體**:

    同樣地，您也可以評估英文版本。

    ```bash
    adk eval weather_agent_en/ weather_agent_en/Weather_evaluation.evalset.json
    ```

### 使用 Pytest 執行測試

除了透過命令列執行評估，您也可以使用 `pytest` 將評估整合到您的測試流程中。本專案包含一個測試檔案，示範如何以程式化的方式執行評估。

**前置需求**:

首先，安裝 `pytest` 與 `pytest-asyncio`：
```bash
pip install pytest pytest-asyncio
```

**執行測試**:

在專案根目錄下執行以下命令：
```bash
pytest
```

Pytest 會自動尋找並執行 `tests/test_agent_evaluation.py` 中定義的測試，這會分別對英文及繁體中文智慧體進行評估。這對於將智慧體評估整合到 CI/CD 管線中非常有用。

### 查看評估結果

評估完成後，詳細的 JSON 報告會自動儲存在各智慧體目錄下的 `.adk/eval_history/` 中。您可以檢視這些檔案來分析智慧體的工具使用情況、回覆內容以及是否符合預期。

### 互動式測試

除了自動化評估，您也可以啟動一個本地網頁介面，直接與您的智慧體進行即時互動。

-   **啟動繁體中文智慧體互動介面**:
    ```bash
    adk web weather_agent/
    ```
-   **啟動英文智慧體互動介面**:
    ```bash
    adk web weather_agent_en/
    ```

執行後，終端機會提供一個網址 (通常是 `http://127.0.0.1:8080`)，在瀏覽器中打開即可開始與您的智慧體對話。

---

## 授權

本專案採用 [Apache 2.0 License](LICENSE) 授權。