# ExperimentHub 

A full-stack A/B testing and experimentation platform that helps companies test product changes safely before releasing them to everyone.

---

##  What Is ExperimentHub?

Companies constantly change things in their apps — new button text, new checkout flows, new pricing layouts, onboarding screens, and more. But releasing a change to 100% of users immediately is risky. If the new version performs worse, the company can lose money, users, or conversions.

ExperimentHub solves this by:

* Splitting traffic between versions, such as 50% seeing the current version and 50% seeing the new version
* Assigning users consistently to the same variant
* Tracking what users actually do, such as clicks, signups, or purchases
* Calculating which version performed better
* Helping teams make data-driven product decisions

It operates behind the scenes. End users do not know they are part of an experiment.

---

##  How It Works

```text
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
Company's app shows the assigned version
        ↓
User performs an action, such as purchase/signup/click
        ↓
Company's app calls ExperimentHub:
POST /events/ → {"event_type": "purchase"}
        ↓
ExperimentHub records the event
        ↓
Admin views analytics → Winner decided 🏆
```

---

##  Demo Flow: Checkout Button Color Test

This demo shows the core backend flow of ExperimentHub: user authentication, experiment creation, variant assignment, event tracking, and analytics.

### 1. Start the backend

```bash
cd backend
source venv/bin/activate
python3 -m uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

### 2. Login and get JWT token

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"your-test-email@example.com","password":"your-test-password"}'
```

The response returns an `access_token`, which is used as a Bearer token for protected endpoints.

### 3. Create an experiment

Create a checkout button A/B test with two variants:

* Blue Button
* Green Button

Traffic split is stored as decimals, so `0.5 + 0.5 = 1.0`.

Example request body:

```json
{
  "name": "Checkout Button Color Test",
  "description": "Test whether a green checkout button improves conversion compared to a blue checkout button.",
  "variants": [
    {
      "name": "Blue Button",
      "description": "Current checkout button color.",
      "traffic_split": 0.5
    },
    {
      "name": "Green Button",
      "description": "New checkout button color.",
      "traffic_split": 0.5
    }
  ]
}
```

### 4. Update experiment status

New experiments start in `draft` status. Before assigning visitors, update the experiment to `running`.

Example request body:

```json
{
  "status": "running"
}
```

### 5. Assign visitors to variants

Visitors were assigned to experiment `2`:

```text
visitor_123 → Blue Button
visitor_124 → Blue Button
visitor_125 → Green Button
visitor_126 → Green Button
```

### 6. Track checkout click events

Checkout click events were tracked for:

```text
visitor_123
visitor_125
visitor_126
```

No event was tracked for `visitor_124`.

Example event body:

```json
{
  "user_id": "visitor_125",
  "experiment_id": 2,
  "event_type": "checkout_click"
}
```

### 7. View analytics

Analytics result:

```json
{
  "experiment_id": 2,
  "experiment_name": "Checkout Button Color Test",
  "event_type": "checkout_click",
  "results": [
    {
      "variant_name": "Blue Button",
      "total_users": 2,
      "conversions": 1,
      "conversion_rate": 50.0
    },
    {
      "variant_name": "Green Button",
      "total_users": 2,
      "conversions": 2,
      "conversion_rate": 100.0
    }
  ],
  "winner": "Green Button"
}
```

### Demo Summary

This confirms that ExperimentHub supports:

* JWT-based authentication
* Protected experiment management
* Variant traffic split validation
* Experiment lifecycle control
* Visitor assignment
* Event tracking
* Conversion analytics
* Winner calculation

---

##  Tech Stack

### Backend

| Tech              | Purpose                         |
| ----------------- | ------------------------------- |
| Python + FastAPI  | REST API framework              |
| PostgreSQL        | Database                        |
| SQLAlchemy        | ORM for database models         |
| Pydantic          | Request and response validation |
| JWT / python-jose | Authentication                  |
| bcrypt / passlib  | Password hashing                |
| httpx             | Webhook delivery                |
| pytest            | Automated testing               |

### Frontend

| Tech         | Purpose          |
| ------------ | ---------------- |
| React        | Dashboard UI     |
| React Router | Page navigation  |
| Axios        | API calls        |
| Recharts     | Analytics charts |

### DevOps

| Tech           | Purpose                     |
| -------------- | --------------------------- |
| Docker         | Containerization            |
| Docker Compose | Multi-service orchestration |

---

##  How To Run Locally

### Option 1 — Docker

Make sure Docker Desktop is running, then run:

```bash
git clone https://github.com/NimishaGeorge18/experimenthub.git
cd ExperimentHub
docker-compose up
```

Everything starts automatically:

* Frontend: `http://localhost:3000`
* Backend API: `http://localhost:8000`
* API Docs: `http://localhost:8000/docs`

### Option 2 — Manual

#### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

Backend API docs:

```text
http://127.0.0.1:8000/docs
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

---

##  API Endpoints

### Auth

| Method | Endpoint         | Description               |
| ------ | ---------------- | ------------------------- |
| POST   | `/auth/register` | Register a new admin user |
| POST   | `/auth/login`    | Login and get JWT token   |

### Users

| Method | Endpoint  | Description |
| ------ | --------- | ----------- |
| GET    | `/users/` | List users  |
| POST   | `/users/` | Create user |

### Experiments

| Method | Endpoint                   | Description              |
| ------ | -------------------------- | ------------------------ |
| POST   | `/experiments/`            | Create experiment        |
| GET    | `/experiments/`            | List all experiments     |
| GET    | `/experiments/{id}`        | Get experiment details   |
| PATCH  | `/experiments/{id}/status` | Update experiment status |

### Assignments

| Method | Endpoint                       | Description                 |
| ------ | ------------------------------ | --------------------------- |
| POST   | `/assignments/{experiment_id}` | Assign visitor to a variant |

### Events

| Method | Endpoint   | Description            |
| ------ | ---------- | ---------------------- |
| POST   | `/events/` | Record a visitor event |

### Analytics

| Method | Endpoint                              | Description              |
| ------ | ------------------------------------- | ------------------------ |
| GET    | `/analytics/{id}?event_type=purchase` | Get conversion analytics |

### Webhooks

| Method | Endpoint                         | Description                |
| ------ | -------------------------------- | -------------------------- |
| POST   | `/webhooks/{experiment_id}`      | Register webhook URL       |
| GET    | `/webhooks/{experiment_id}`      | List webhooks              |
| GET    | `/webhooks/{experiment_id}/logs` | View webhook delivery logs |

### Health Check

| Method | Endpoint  | Description          |
| ------ | --------- | -------------------- |
| GET    | `/health` | Check backend health |

---

##  Running Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

Tests cover:

* Auth: register, login, wrong password
* Experiments: create, list, status update
* Assignments: assign user and maintain consistency
* Events: record events and reject invalid/unassigned users
* Analytics: calculate conversion rates
* Webhooks: register webhooks and view delivery logs

---

##  How A/B Testing Works

### Traffic Splitting

When a visitor is assigned, the system uses the configured traffic split to decide which variant the visitor should receive.

Example:

```text
Variants:
Blue Button  = 50%
Green Button = 50%

Traffic split:
Blue Button  = 0.5
Green Button = 0.5
Total        = 1.0
```

This ensures traffic is distributed according to the experiment setup.

### Consistency

Once a visitor is assigned to a variant, they continue receiving the same variant for that experiment. The assignment is stored in the database and reused on future calls.

This prevents users from seeing different versions of the same experiment across sessions.

### Event Tracking

After a visitor performs an action, such as clicking checkout, the company’s app sends an event to ExperimentHub.

Example:

```json
{
  "user_id": "visitor_123",
  "experiment_id": 2,
  "event_type": "checkout_click"
}
```

ExperimentHub links the event to the visitor’s assigned variant.

### Conversion Rate

```text
Conversion Rate = (Users who triggered event / Total assigned users) × 100
```

Example:

```text
Blue Button:
1 checkout click / 2 assigned users = 50%

Green Button:
2 checkout clicks / 2 assigned users = 100%

Winner: Green Button 🏆
```

---

##  What I Learned

* Designing and building a REST API from scratch with FastAPI
* Structuring a backend using routes, schemas, models, services, and database layers
* Database modeling with SQLAlchemy and PostgreSQL
* User authentication using JWT
* Secure password hashing with bcrypt/passlib
* Protecting API endpoints with Bearer token authentication
* Building core A/B testing logic such as experiment creation, traffic splitting, assignment, event tracking, and analytics
* Validating experiment configuration, including traffic splits adding up to 1.0
* Managing experiment lifecycle states such as draft and running
* Writing automated tests with pytest
* Creating a React dashboard structure for frontend integration
* Using Docker and Docker Compose for local development

---

##  Project Structure

```text
ExperimentHub/
├── backend/
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # JWT and settings
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

##  Future Improvements

* Fix Swagger authorization flow so protected endpoints can be tested directly from the Swagger Authorize button
* Add more frontend screens for experiment creation, assignment testing, and analytics visualization
* Add charts for conversion rates using Recharts
* Add role-based access control for admin users
* Improve analytics with statistical significance calculations
* Add deployment instructions
* Add CI/CD pipeline for automated testing

---
