# Указываем базовый образ Python
FROM python:3.9

# Устанавливаем рабочий каталог в контейнере
WORKDIR /app

# Копируем файл с зависимостями (requirements.txt) в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "main.py"]
