#1st step : build 
FROM python:3.9-slim

#setting woring directory
WORKDIR /app

#copying requirements to run app
COPY requirements.txt .

#command to install requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
#stage 2 : Production

EXPOSE 5000

CMD ["python", "application.py"]


