
# An URL Shortener
---
## Tech Stack
- Backend: Go Fiber
- Frontend: React Typescript
- Database: Postgres
---
## Feature
- Simple Authentication
- CRUD URL Shortener
- Each URL Shortener has how many click on it
---
## Model
- Auth
- Refresh Token
- Verification Token
- Ledger

### Base Entity
- UUID 
- CreatedAt: DateTime
- updatedAt: DateTime
- deletedAt: DateTime

### Auth
- BaseEntity
- username: string
- password: string
- isVerified: boolean
- isActive: boolean

### Verification Token
- BaseEntity
- AuthID : uuid
- token: string
- expiredAt: DateTime
- isRevoke: boolean

### Refresh Token
- BaseEntity
- token: string
- expiredAt: DateTime
- isRevoke: boolean
- AuthID: uuid

ShortLink
- BaseEntity
- OwnBy: UUID
- view: Integer
- target_url : string
- short_url : string
- type: Enum(CUSTOM, RANDOM)


See other project: [[Web app for homelab]]