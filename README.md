# Free Fly Bot

Дискорд бот для отслеживания событий и пилотов.

## Минимум работ

Бот должен отслеживать время до ближайшего события, параллельно принимать команды о создании удалении или изменения новых.

### Что нужно еще сделать

- [ ] events, addevent, delevent: добавить фильтр на выдачу пользователю только тех событий к которому он имеет допуск. Копатель не должнен **видеть** и **создавать** события для производственников
- [ ] переделать датаклассы в обычные классы с проверкой при присваивание значений
- [x] создать ui на команду add_event
- [ ] перенести логику из команды test в add_event, добавление события в базу данных
- [x] добавить обработку ошибки add event modal
- [x] закрывать взаимодействие modal on_conferm
- [x] закрывать взаимодействие modal on_timeout
- [x] отслеживать нажатие на кнопку только от пользователя
- [x] написать парсер аргументов полученных от event_modal: event_date и event_time в datetime
- [ ] таймер для отслеживания ближайшего события

### Команды

- /help
- /eventslist - список всех событий на текущем сервере
- /addevent - создать новое событие на текущем сервере
- /deleteevent - удалить событие на текущем сервере

- /types - типы евентов на сервере
- /addtype - добавить тип на сервер
- /deletetype - удалить тип на сервере
- /updatetype - изменить тип на сервере

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
