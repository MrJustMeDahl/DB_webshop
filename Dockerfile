FROM python:3.11-slim

# Install required Python libraries
RUN pip install redis==5.2.1
RUN pip install mysql-connector-python==9.3.0
RUN pip install pymongo==4.12.1

WORKDIR /app
