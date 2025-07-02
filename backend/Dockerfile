# Python 3.11 slim image kullan
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Python bağımlılıklarını kur
RUN pip install fastapi uvicorn pydantic

# Uygulama kodlarını kopyala
COPY . .

# Port 8000'i aç
EXPOSE 8000

# Uygulamayı çalıştır
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 