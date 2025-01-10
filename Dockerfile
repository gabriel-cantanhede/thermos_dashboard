FROM python:3.12-slim

# Expose port you want your app on
EXPOSE 8501

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run
ENTRYPOINT ["streamlit", "run", "main_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
