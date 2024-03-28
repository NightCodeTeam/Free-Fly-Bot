CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    event_name VARCHAR(30),
    type_id INTEGER NOT NULL,
    comment VARCHAR(300),
    event_time TIMESTAMP NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id),
    FOREIGN KEY(type_id) REFERENCES types(type_id));

CREATE TABLE IF NOT EXISTS types (
    type_id INTEGER PRIMARY KEY,
    server_id INTEGER NOT NULL,
    type_name VARCHAR(15) NOT NULL, 
    channel VARCHAR(30) NOT NULL,
    role_name VARCHAR(30) NOT NULL,
    FOREIGN KEY(server_id) REFERENCES servers(server_id));

CREATE TABLE IF NOT EXISTS servers (
    server_id INTEGER PRIMARY KEY,
    server_name VARCHAR(50) UNIQUE);
