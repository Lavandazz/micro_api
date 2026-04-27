class BaseConfig:
    API_TITLE = "Kitchen API"
    API_VERSION = "V1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_JSON_PATH = "openapi/kitchen.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "/redoc"
    OPENAPI_REDOC_URL = "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js" # Путь к скрипту для рендеринга redoc
    OPENAPI_SWAGGER_UI_PATH = '/docs/kitchen'  # Путь к скрипту
    OPENAPI_SWAGGER_UI_URL = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/' # Перенаправление к swagger
    