# Secrets

Этот проект предназначен для управления секретами с использованием Python и Docker Compose.

## Установка и запуск

1. Убедитесь, что у вас установлены [Docker](https://www.docker.com/) и [Docker Compose](https://docs.docker.com/compose/).
2. Клонируйте репозиторий проекта:
    ```bash
    git clone https://github.com/kreengg/secrets-test-task.git
    cd secrets-test-task
    ```
3. Создайте `.env` файл с переменными указаными в `.env.example` 
4. Запустите контейнеры с помощью Docker Compose:
    ```bash
    docker-compose up -d
    ```

## Использование

После запуска приложения по адресу `http://localhost:8000/api/docs` можно увидеть Swagger документацию
