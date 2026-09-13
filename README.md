# MarketPlus AI

An automated, serverless financial monitoring pipeline that tracks customized stock watchlists, detects multi-metric market dips using DuckDB analytical queries, enriches alerts with Google Gemini contextual intelligence, and dispatches automated notifications via GitHub Actions.

---

## Architecture & Data Flow

```
[ Streamlit Dashboard ] ──(Manage Watchlist & Criteria)──► [ Persistent Store / Cloud / Git ]
                                                                      │
                                                                      ▼
[ GitHub Actions Cron ] ──────(Daily Market Close Run)───► [ Python Orchestrator ]
                                                                      │
                                   ┌──────────────────────────────────┴────────────────────────────────┐
                                   ▼                                  ▼                                ▼
                         [ Financial Data API ]             [ In-Process DuckDB ]            [ Google Gemini LLM ]
                         (Daily OHLCV & Ratios)             (Lookback Window & Drop           (Executive Summary &
                                                              Calculations)                     Market Context)
                                                                                                       │
                                                                                                       ▼
                                                                                             [ Automated Email Alert ]

```

1. **Watchlist & Thresholds:** Configure watchlists, lookback periods, drop thresholds, and optional technical indicators (Moving Averages, P/E ratios) via the Streamlit interface.
2. **Scheduled Orchestration:** GitHub Actions triggers a headless pipeline daily after market close.
3. **Analytical Processing:** DuckDB performs in-process window calculations on historical price metrics to identify stocks exceeding drop criteria.
4. **Contextual AI Analysis:** Google Gemini generates a concise market brief explaining recent price drops and technical context.
5. **Notification Delivery:** Formatted alert emails are automatically dispatched with entry prices, lookback baselines, and MarketPlus AI's contextual analysis.

---

## Tech Stack

* **Data Engine & Transformation:** DuckDB
* **Orchestration & CI/CD:** GitHub Actions (Scheduled Cron)
* **AI & Contextual Summaries:** Google Gemini API
* **Interactive UI:** Streamlit
* **Core Language:** Python 3.11+
* **Alert Delivery:** SMTP / Email Dispatcher

---

## Project Structure

```text
marketplus-ai/
├── .github/
│   └── workflows/
│       └── daily_stock_alert.yml   # Scheduled CI/CD automation workflow
├── config/
│   ├── alert_rules.yaml            # Thresholds, lookback parameters, and metrics
│   └── settings.py                 # Environment variables and credential manager
├── data/                           # Local database store or historical cache
├── src/
│   ├── data_fetcher.py             # Pulls market data and ratios
│   ├── db_manager.py               # DuckDB analytical queries & schema
│   ├── alert_engine.py             # Evaluates drops and filtering logic
│   ├── gemini_analyzer.py          # Gemini API prompt formatting & parsing
│   ├── notifier.py                 # HTML email generation & SMTP sending
│   └── pipeline.py                 # Core headless execution entry point
├── ui/
│   └── app.py                      # Streamlit dashboard for watchlist management
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

```

---

## Key Features

* **Custom Multi-Metric Criteria:** Alert triggers are not limited to single-day drops; configure lookback periods (e.g., 3-day or 7-day cumulative declines) combined with moving averages or valuation indicators.
* **In-Process Analytical Engine:** Utilizes DuckDB for fast vector/window aggregations directly inside the execution runner without dedicated database server costs.
* **LLM Market Summaries:** MarketPlus AI delivers human-readable context alongside raw percentage drops.
* **Serverless Execution:** Runs purely on ephemeral GitHub Actions compute on a schedule.

---

## Setup & Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/marketplus-ai.git
cd marketplus-ai

```

### 2. Configure Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Set Environment Variables

Copy `.env.example` to `.env` and provide your credentials:

```bash
cp .env.example .env

```

Populate the following:

* `GEMINI_API_KEY`
* `SMTP_SERVER`
* `SMTP_PORT`
* `SMTP_USER`
* `SMTP_PASSWORD`
* `NOTIFICATION_RECIPIENT`

---

## Running the Application

* **Launch Watchlist Dashboard:**
```bash
streamlit run ui/app.py

```


* **Run the Pipeline Manually:**
```bash
python -m src.pipeline

```



---

## GitHub Actions Deployment

To run daily alerts automatically:

1. Navigate to **Settings > Secrets and variables > Actions** in your GitHub repository.
2. Add the required repository secrets (`GEMINI_API_KEY`, `SMTP_USER`, `SMTP_PASSWORD`, etc.).
3. The workflow defined in `.github/workflows/daily_stock_alert.yml` will automatically trigger on the configured cron schedule.