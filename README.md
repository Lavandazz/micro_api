# micro_api
## Проект для изучения микросервисной архитектуры.
### Используются технологии:
- FastAPI
- Uvicorn
- pipenv


### Активация виртуальной среды с использованием pipenv:
`pipenv shell`
### Запуск сервера:
`uvicorn ch02.orders.app:app --reload`
### Или запуск через конфигурацию:
script: .../.local/share/virtualenvs/api-.../bin/uvicorn
`ch02.orders.app:app --reload`
