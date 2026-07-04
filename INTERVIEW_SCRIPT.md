# ExperimentHub Interview Script

## 30-Second Summary

ExperimentHub is a full-stack A/B testing and experimentation platform that helps companies test product changes safely before rolling them out to all users. It allows users to create experiments with multiple variants, assign visitors to variants, track events like clicks or purchases, and calculate analytics such as conversion rate and winning variant.

## Why I Built It

I built this project because many companies do not release product changes directly to all users. They use controlled experiments to compare versions and make data-driven decisions. I wanted to build the backend logic behind that process.

## Main Features

- User registration and login using JWT authentication
- Protected experiment management
- Experiment creation with multiple variants
- Traffic split validation
- Experiment lifecycle control such as draft and running
- Visitor assignment to variants
- Event tracking
- Conversion analytics
- Winner calculation

## Demo Example

I created a checkout button color experiment with two variants:

- Blue Button
- Green Button

The system assigned visitors to each variant, tracked checkout click events, calculated conversion rates, and selected the winning variant.

Final result:

- Blue Button: 2 users, 1 conversion, 50% conversion rate
- Green Button: 2 users, 2 conversions, 100% conversion rate
- Winner: Green Button

## Technical Explanation

The backend is built with FastAPI, PostgreSQL, SQLAlchemy, and Pydantic. Authentication is handled using JWT tokens. Protected endpoints require a Bearer token. The database stores users, experiments, variants, assignments, events, webhooks, and analytics-related data.

When a visitor is assigned to an experiment, the backend selects a variant based on the configured traffic split. Once assigned, the visitor stays in the same variant for consistency. When that visitor performs an event, such as checkout_click, the event is linked to their assigned variant. The analytics endpoint then calculates total assigned users, conversions, conversion rate, and the current winner.

## Challenges I Faced

One challenge was testing protected endpoints. Login worked and returned a JWT token, but Swagger Authorize did not work properly because the Swagger OAuth flow expected form-style username/password while my login endpoint used JSON email/password. I worked around this by testing protected endpoints using curl with the Bearer token. This also helped me understand authentication flow better.

Another challenge was traffic split validation. Initially I tested variants with 50 and 50, but the backend expected decimals that add up to 1.0, so the correct values were 0.5 and 0.5. This helped ensure experiment configuration stays valid.

## What I Learned

I learned how to design a real backend system with authentication, protected routes, database models, business logic, validation, and analytics. I also learned how A/B testing platforms manage experiment lifecycle, assignment consistency, event tracking, and conversion metrics.

## Future Improvements

- Fix Swagger authorization flow
- Improve frontend dashboard
- Add analytics charts
- Add statistical significance
- Add deployment
- Add CI/CD pipeline