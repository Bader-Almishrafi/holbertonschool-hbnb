# HBnB Database ER Diagram

```mermaid
erDiagram

    USERS {
        string id PK
        string first_name
        string last_name
        string email UNIQUE
        string password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    PLACES {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
        datetime created_at
        datetime updated_at
    }

    REVIEWS {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
        datetime created_at
        datetime updated_at
    }

    AMENITIES {
        string id PK
        string name UNIQUE
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        string place_id PK, FK
        string amenity_id PK, FK
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : has
    PLACES ||--o{ PLACE_AMENITY : contains
    AMENITIES ||--o{ PLACE_AMENITY : linked_to

---

### What this diagram represents

Entities included in the diagram:

- USERS
- PLACES
- REVIEWS
- AMENITIES
- PLACE_AMENITY (join table)

Relationships:

User → Place  
One user can own many places.

User → Review  
One user can write many reviews.

Place → Review  
One place can have many reviews.

Place ↔ Amenity  
Many-to-many relationship implemented through the `PLACE_AMENITY` table.

---

### How to preview the diagram

Option 1 (recommended)

Open the Mermaid Live Editor:

https://mermaid.live

Paste the diagram code to visualize it.

Option 2

GitHub automatically renders Mermaid diagrams inside Markdown files. Just push the file to your repository.

---

If you want, I can also give you a **clean final project checklist** (10 items to verify before submission) so you avoid losing points in Holberton’s checker.
