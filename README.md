# Установка зависимостей

1) pipenv lock - создать файл с информацией о пакетах
2) pipenv install --ignore-pipfile - установить пакеты в окружение
3) pipenv install --dev - установить пакеты в окружение из катгории [dev-packages]

# Установка постгреса

1) docker run -d -p 5432:5432  -e POSTGRES_PASSWORD=pass --name postgres postgres - создать контейнер с бд
2) docker exec -it postgres bash - открыть консоль контейнера
3) psql -U postgres - войти в базу данных