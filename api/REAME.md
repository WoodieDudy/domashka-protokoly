# VK Friends

Cервер на FastAPI для просмотра списока друзей ВКонтакте

## Зависимости

```bash
pip install fastapi uvicorn requests
```

## Запуск

1. Зайти в папку api

```bash
cd api
```

2. В файле token.py написать свой токен от вк


3. Запустить сервер:
 ```
 uvicorn vk_friends:app --reload
 ```

4. Перейти по адресу http://localhost:8000/
