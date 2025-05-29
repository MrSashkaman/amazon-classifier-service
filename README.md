# Inference сервис для Multi-label классификации снимков Амазонки

Сервис для классификации спутниковых снимков тропических лесов Амазонки с использованием FastAPI и ONNX-модели.

## 🚀 Демо-версия

Документация Swagger доступна по адресу:  
http://91.206.15.25:8032/docs

## 🛠️ Локальная установка
### Требования
- Python 3.12
- Docker 20.10+
- Make

### 0. Подготовка окружения и установка зависимостей:
```bash
python3.12 -m venv venv
source venv/bin/activate
make install
```

### 1. Загрузка весов модели:
Модель предварительно обучена и сохранена в формате .onnx
```bash
make download_weights
```

### 4. Запуск сервиса:
- Без Docker:
    ```bash
    make run_app  # Сервис доступен на http://localhost:5004
    ```
- C Docker:
    ```bash
    make build && make docker.run-locally  # Порт указан в APP_PORT (по умолчанию 5004)
    ```
## 🧪 Тестирование
Команда запустит юнит и интеграционные тесты из директории tests/
```bash
make run_all_tests  # Запуск юнит- и интеграционных тестов
make lint          # Проверка стиля кода
```

## 🐳 Docker образы
- Production: amazon-clf:prod
- Development: amazon-clf:dev
### Сборка образов:
```bash
make build
```

### Проверка сборки:
```bash
make hw.docker-check  # Запуск тестов и линтера внутри контейнера
```

## ☁️ Развертывание на сервере с помощью Ansible
- деплой:
    ```bash
    make deploy
    ```
- Остановка сервиса и удаление файлов:
    ```bash
    make destroy
    ```

## ☁️ CI/CD
Настроен процесс развертывания с помощью gitlab пайплайнов
