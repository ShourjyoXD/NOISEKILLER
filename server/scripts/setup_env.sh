# 1. Create a virtual environment
python3 -m venv venv

# 2. Activate the environment
# For Mac/Linux:
source venv/bin/activate
# For Windows (use this instead):
# .\venv\Scripts\activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install Core Dependencies
pip install fastapi \
            uvicorn \
            pydantic \
            python-dotenv \
            openai \
            langchain \
            langchain-openai \
            httpx \
            pytest