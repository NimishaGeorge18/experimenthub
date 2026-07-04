# ExperimentHub 🧪

A full-stack A/B testing and experimentation platform that helps companies test product changes safely before releasing them to everyone.

---

## 🌍 What Is ExperimentHub?

Companies constantly change things in their apps — new button text, new checkout flows, pricing layouts, onboarding screens, and more. But releasing a change to 100% of users immediately is risky. If the new version performs worse, the company can lose money, users, or conversions.

ExperimentHub solves this by:

* Splitting traffic between different versions of a feature
* Assigning visitors consistently to the same variant
* Tracking user actions such as clicks, signups, and purchases
* Calculating conversion rates for each variant
* Identifying the winning variant based on performance
* Helping teams make data-driven product decisions

It operates behind the scenes. End users do not know they are part of an experiment.

---

## 🏗️ How It Works

```text
Company defines an experiment
        ↓
User opens the company's app
        ↓
Company's app calls ExperimentHub:
POST /assignments/{experiment_id}
        ↓
ExperimentHub assigns the user to a variant
        ↓
Company's app shows the assigned version
        ↓
User performs an action such as click, signup, or purchase
        ↓
Company's app calls ExperimentHub:
POST /events/
        ↓
ExperimentHub records the event
        ↓
Admin views analytics and winner is calculated
```

---

## 🎯 Demo Flow: Checkout Button Color Test

This demo shows the core backend flow of ExperimentHub: user authentication, experiment creation, visitor assignment, event tracking, analytics, and winner calculation.

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
* React frontend dashboard for viewing experiments
* Frontend experiment creation flow
* Frontend experiment status updates
* Demo Tools UI for assigning visitors to variants
* Demo Tools UI for tracking visitor events
* Frontend analytics chart and conversion table using Recharts

---

## 🖥️ Frontend Demo Tools

The React frontend includes an admin dashboard for managing and testing experiments.

From the frontend, an admin can:

* View all experiments
* Create a new experiment with variants and traffic splits
* Open an experiment detail page
* Start, pause, resume, or complete an experiment
* View experiment variants and traffic distribution
* Assign demo visitors to variants
* Track demo events for assigned visitors
* Analyze conversion rates using charts and tables

### Example Frontend Demo

For the `Homepage CTA Text Test`, two variants were created:

* Start Free Trial
* Get Started

Using the Demo Tools section, visitors were assigned to variants and `signup_click` events were tracked.

Example result:

```text
Start Free Trial:
3 users, 1 conversion = 33.33%

Get Started:
4 users, 1 conversion = 25%

Winner: Start Free Trial
```

This confirms that the frontend is connected to the backend and can demonstrate the full experimentation flow from the browser.

---

## 🛠️ Tech Stack

### Backend

| Tech              | Purpose                         |
| ----------------- | ------------------------------- |
| Python + FastAPI  | REST API framework              |
| PostgreSQL        | Database                        |
| SQLAlchemy        | ORM for database models         |
| Pydantic          | Request and response validation |
| JWT / python-jose | Authentication                  |
| bcrypt / passlib  | Password hashing                |
| pytest            | Automated testing               |
| httpx             | Webhook delivery                |

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

## 🚀 How To Run Locally

### Option 1 — Manual Setup

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

Open a new terminal tab:

```bash
cd frontend
npm install
npm start
```

Frontend app:

```text
http://localhost:3000
```

### Option 2 — Docker

Make sure Docker Desktop is running, then run:

```bash
git clone https://github.com/NimishaGeorge18/experimenthub.git
cd ExperimentHub
docker-compose up
```

Expected local URLs:

* Frontend: `http://localhost:3000`
* Backend API: `http://localhost:8000`
* API Docs: `http://localhost:8000/docs`

---

## 📡 API Endpoints

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

## 🧪 Running Tests

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

## 📊 How A/B Testing Works

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

Winner: Green Button
```

---

## 💡 What I Learned

* Designing and building a REST API from scratch with FastAPI
* Structuring a backend using routes, schemas, models, services, and database layers
* Database modeling with SQLAlchemy and PostgreSQL
* User authentication using JWT
* Secure password hashing with bcrypt/passlib
* Protecting API endpoints with Bearer token authentication
* Connecting a React frontend to a protected FastAPI backend using JWT tokens
* Building frontend demo tools for testing assignment and event tracking
* Displaying conversion analytics with Recharts
* Building core A/B testing logic such as experiment creation, traffic splitting, assignment, event tracking, and analytics
* Validating experiment configuration, including traffic splits adding up to 1.0
* Managing experiment lifecycle states such as draft, running, paused, and completed
* Debugging frontend/backend integration issues such as missing backend server, expired tokens, and protected route behavior
* Writing automated tests with pytest
* Using Docker and Docker Compose for local development

---

## 📁 Project Structure

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
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Login, Register, Experiments, Details
│   │   ├── App.js        # Routing
│   │   └── index.js      # React entry point
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🔮 Future Improvements

* Fix Swagger authorization flow so protected endpoints can be tested directly from the Swagger Authorize button
* Polish frontend UI and improve error/loading states
* Add screenshots or GIF demo to README
* Add deployment instructions for frontend and backend
* Add role-based access control for admin users
* Improve analytics with statistical significance calculations
* Add CI/CD pipeline for automated testing
* Add production-ready environment variable setup
* Add better logging and monitoring

---


