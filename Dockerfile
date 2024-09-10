# Python bazaviy imidjini o'rnatamiz
FROM python:3.11-slim

# Ish katalogini yaratamiz
WORKDIR /app

# Zarur fayllarni konteyner ichiga ko'chiramiz
COPY requirements.txt .

# Zarur paketlarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Loyihani konteyner ichiga ko'chiramiz
COPY . .

# Django serverni ishga tushiramiz
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
