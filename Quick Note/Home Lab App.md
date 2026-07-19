# Personal Server
it just a personal server that can host many application

## Home Lab Personal Project : 8000 to 9000

| Service           | Sub Domain | Port |
| ----------------- | ---------- | ---- |
| gateway           | api        | 8000 |
| service discovery | discovery  | 8999 |
| keycloak          | auth       | 8001 |
|                   |            |      |
|                   |            |      |
## Home Lab Self host App : 7000 to 8000

| Name         | Sub Domain | Port |
| ------------ | ---------- | ---- |
| Adguard home | adguard    | 7000 |
| Portainer    | container  | 7001 |

## Home Lab Database : Depend on default port

| DB       | Sub Domain | Port                          |
| -------- | ---------- | ----------------------------- |
| Postgres | postgres   | 5432                          |
| Redis    | redis      | 6379                          |
| MongoDB  | mongo      | 27017                         |
| MinIO    | storage    | 9000 (s3 api), 9001 (console) |
