# ExperimentHub 🧪

A full-stack A/B testing and experimentation platform that helps companies test changes safely before releasing them to everyone.

---

## 🌍 What Is ExperimentHub?

Companies constantly change things in their apps — new button text, new checkout flows, new pricing layouts. But releasing a change to 100% of users immediately is risky. If it performs worse, they lose money or customers.

ExperimentHub solves this by:
- Splitting traffic between versions (e.g. 50% see old, 50% see new)
- Tracking what users actually do (purchase, signup, click)
- Calculating which version performed better
- Letting companies make data-driven decisions

It operates entirely behind the scenes. End users never know they're being tested.

---

## 🏗️ How It Works
```
Company defines experiment
        ↓
User opens company's app
        ↓
Company's app calls ExperimentHub:
POST /assignments/1 → {"user_id": "user_123"}
        ↓
ExperimentHub responds:
{"variant_name": "Treatment"}
        ↓
Company's app shows the right version
        ↓
User makes a purchase
        ↓
Company's app calls ExperimentHub:
POST /events/ → {"event_type": "purchase"}
        ↓
ExperimentHub records it
        ↓
Admin views analytics → Winner decided 🏆
```

---

## 🛠️ Tech Stack

### Backend
| Tech | Purpose |
|---|---|
| Python + FastAPI | REST API framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM (database models) |
| Pydantic | Request/response validation |
| JWT (python-jose) | Authentication |
| bcrypt (passlib) | Password hashing |
| httpx | Webhook delivery |
| pytest | Automated testing |

### Frontend
| Tech | Purpose |
|---|---|
| React | Dashboard UI |
| React Router | Page navigation |
| Axios | API calls |
| Recharts | Analytics charts |

### DevOps
| Tech | Purpose |
|---|---|
| Docker | Containerization |
| Docker Compose | Multi-service orchestration |

---

## 🚀 How To Run Locally

### Option 1 — Docker (Recommended)

Make sure Docker Desktop is running, then:
```bash
git clone https://github.com/NimishaGeorge18/experimenthub.git
cd ExperimentHub
docker-compose up
```

That's it. Everything starts automatically:
- Frontend → http://localhost:3000
- Backend API → http://localhost:8000
- API Docs → http://localhost:8000/docs

### Option 2 — Manual

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new admin |
| POST | `/auth/login` | Login and get JWT token |

### Experiments
| Method | Endpoint | Description |
|---|---|---|
| POST | `/experiments/` | Create experiment |
| GET | `/experiments/` | List all experiments |
| GET | `/experiments/{id}` | Get experiment details |
| PATCH | `/experiments/{id}/status` | Start / pause / complete |

### Assignment (used by company's app)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/assignments/{experiment_id}` | Assign user to variant |

### Events (used by company's app)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/events/` | Record a user event |

### Analytics
| Method | Endpoint | Description |
|---|---|---|
| GET | `/analytics/{id}?event_type=purchase` | Get conversion rates |

### Webhooks
| Method | Endpoint | Description |
|---|---|---|
| POST | `/webhooks/{experiment_id}` | Register webhook URL |
| GET | `/webhooks/{experiment_id}/logs` | View delivery history |

---

## 🧪 Running Tests
```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

**17 tests covering:**
- Auth (register, login, wrong password)
- Experiments (create, list, status update)
- Assignments (assign user, consistency)
- Events (record, unassigned user rejection)
- Analytics (conversion rate calculation)

---

## 📊 How A/B Testing Works

### Traffic Splitting
When a user is assigned, a random number between 0 and 1 is generated. The user is placed in the variant whose cumulative traffic split covers that number:
```
Variants: Control=50%, Treatment=50%
Random roll: 0.73

Control cumulative:   0.50 → 0.73 > 0.50, keep going
Treatment cumulative: 1.00 → 0.73 < 1.00, assign Treatment ✅
```

This naturally produces the correct distribution at scale.

### Consistency
Once a user is assigned, they always get the same variant. The assignment is stored in the database and returned on every subsequent call. This ensures test integrity.

### Conversion Rate
```
Conversion Rate = (Users who triggered event / Total assigned users) × 100

Control:   120 purchases / 1000 users = 12%
Treatment: 170 purchases / 1000 users = 17%

Winner: Treatment 🏆
```

---

## 💡 What I Learned

- Designing and building a REST API from scratch with FastAPI
- Database modeling with SQLAlchemy and PostgreSQL
- JWT authentication and secure password hashing
- Core A/B testing logic — traffic splitting and conversion tracking
- Separating concerns across models, schemas, services, and API layers
- Writing meaningful automated tests with pytest
- Building a React frontend with protected routes and API integration
- Data visualization with Recharts
- Containerizing a multi-service application with Docker Compose
- Webhook design and delivery logging

---

## 📁 Project Structure
```
ExperimentHub/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # JWT + settings
│   │   ├── db/           # Database connection
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── webhooks/     # Webhook sender
│   ├── tests/            # pytest tests
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/          # Axios API calls
│   │   ├── pages/        # Login, Experiments, Analytics
│   │   └── App.js        # Routing
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

Built with ❤️ by Nimisha George