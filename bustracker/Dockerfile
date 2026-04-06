FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=bustracker.settings_production
ENV SECRET_KEY=temp-build-key-not-used-in-production
ENV DATABASE_URL=sqlite:///tmp/temp.db

RUN python manage.py collectstatic --noinput

RUN sed -i 's/\r//' start.sh && chmod +x start.sh && cat start.sh

EXPOSE 8000

CMD ["/bin/bash", "start.sh"]