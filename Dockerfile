FROM python:3.11-slim

WORKDIR /app

# Install app dependencies
RUN pip install --no-cache-dir flask "openai<1"

# Copy project files
COPY . /app

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

CMD ["flask", "run"]
