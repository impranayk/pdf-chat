@echo off
rem Starts the "Chat with your PDF" app (reel #39) fully offline on port 8790.
cd /d "%~dp0"
set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1
set ANONYMIZED_TELEMETRY=False
python -m streamlit run app.py --server.port 8790 --server.headless true --browser.gatherUsageStats false
