FROM python:3.12.5

# Expose port you want your app on
EXPOSE 5900

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY .streamlit .streamlit
COPY assets assets
COPY control control
COPY model model
COPY views views
COPY style.css style.css
COPY main_app.py main_app.py
WORKDIR .

# Run
ENTRYPOINT [“streamlit”, “run”, “main_app.py”, “–server.port=5900”, “–server.address=0.0.0.0”]