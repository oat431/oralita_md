# A Ledger Application
---
## Tech Stack
- Backend: Go Fiber
- Frontend: React Typescript
- Database: Postgres
---
## Feature
- Simple Authentication
- CRUD Money Accounting
- Daily Summary via email
- Weekly Summary via email
- Monthly Summary via email
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

### Ledger
- BaseEntity
- OwnBy: UUID
- No : Integer
- Description: Integer
- Value: BigNumber
- Type: Enum(INCOME, SPENDING)
- Balance : Bignumber

### Subscription
- BaseEntity
- OwnBy: UUID
- No. :Integer
- Service: string
- description: string
- type: Enum(Credit, Bank)

See other project: [[Web app for homelab]]