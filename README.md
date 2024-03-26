# Free Fly Bot

Дискорд бот для отслеживания событий и пилотов.

## Минимум работ

Бот должен отслеживать время до ближайшего события, параллельно принимать команды о создании удалении или изменения новых.

### Команды

- /help
- /eventslist - список всех событий на текущем сервере
- /addevent - создать новое событие на текущем сервере
- /updateevent - изменить событие на текущем сервере
- /deleteevent - удалить событие на текущем сервере

- /types - типы евентов на сервере
- /addtype - добавить тип на сервер
- /deletetype - удалить тип на сервере

-

### Таблицы SQL

#### Events

| COLUMN NAME | TYPE    | ADT         |
|------------|----------|-------------|
| event_id   | INTEGER  | PRIMARY KEY |
| server_id  | INTEGER  | NOT NULL    |
| event_name | TEXT     | NOT NULL    |
| type_id    | INTEGER  | NOT NULL    |
| comment    | TEXT     |             |
| event_time | DATETIME | NOT NULL    |

#### Types

| COLUMN NAME | TYPE    | ADT         |
|-----------|---------|-------------|
| type_id   | INTEGER | PRIMARY KEY |
| server_id | INTEGER | NOT NULL    |
| type_name | TEXT    | NOT NULL    |
| channel   | TEXT    | NOT NULL    |

#### Discord servers

| COLUMN NAME | TYPE    | ADT         |
|-------------|---------|-------------|
| server_id   | INTEGER | PRIMARY KEY |
| server_name | TEXT    | NOT NULL    |

#### Pilot

| COLUMN NAME | TYPE    | ADT         |
|--------------|---------|-------------|
| pilot_id     | INTEGER | PRIMARY KEY |
| name         | TEXT    | NOT NULL    |
| discord_nick | TEXT    | NOT NULL    |

#### Pilot Role

| COLUMN NAME | TYPE    | ADT         |
|----------|---------|-------------|
| pilot_id | INTEGER | PRIMARY KEY |
| type_id  | INTEGER | NOT NULL    |

### Реализация

Содержится 2 потока:

1) Поток обрабатывающий работу с пользователями
2) Потом с таймером отсчета

Бот на discord.py

База данных aiosqlite
