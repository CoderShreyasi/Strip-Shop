Simple Stripe Shop

A minimal Stripe-powered e-commerce project built with Django, allowing users to view products, purchase them via Stripe Checkout, and view their order history.

Assumptions & Choices:
Tech Stack: Django 4.x, Python 3.11, PostgreSQL 15, Stripe API, Bootstrap 5 for UI.
Stripe Integration: Used Stripe Checkout for simplicity and secure payments.
Database: PostgreSQL for production-similar environment; local SQLite could be used for testing.
Docker: Project uses Docker and docker-compose to manage both Django app and PostgreSQL DB.
UI: Bootstrap 5, cards for products, responsive design. Simple UX prioritizing functionality over visual polish.
Quantity & Orders: Users can choose quantity before checkout. Completed orders are displayed in “My Orders.”

Setup & Run Steps
1. Clone Repository
git clone <your-repo-url>
cd Stripe_shop

2. Environment Variables

Create a .env file in the root directory:

POSTGRES_DB=stripe_shop_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
STRIPE_PUB_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...


Replace STRIPE_PUB_KEY and STRIPE_SECRET_KEY with your Stripe test keys.

3. Docker Setup

Build and run containers:

docker compose up -d --build


Check running containers:

docker compose ps


You should see:

django_stripe_app running on port 8000

stripe_shop-db-1 running PostgreSQL

4. Database Setup

Run migrations inside Django container:

docker compose exec django_stripe_app python manage.py makemigrations
docker compose exec django_stripe_app python manage.py migrate

5. Create Superuser (optional, for admin access)
docker compose exec django_stripe_app python manage.py createsuperuser


Access admin at http://127.0.0.1:8000/admin/

6. Access the Application

Open in browser:

http://127.0.0.1:8000/


Browse products

Buy products using Stripe Checkout

View completed orders under My Orders

7. Stopping the Application
docker compose down


This stops and removes the containers.

Code Notes & Quality

Code Structure: Follows Django standard project structure (stripe_shop_project/, stripe_shop_app/).

Separation of Concerns: Views handle business logic, templates handle presentation, models store data.

Stripe Checkout: Implemented via JS + Django POST request to /create-checkout-session/.

Docker: Containerized both app and DB for reproducibility.

Error Handling: Basic checks for DB readiness (wait-for-db.sh), quantity defaults, and CSRF protection.

UI/UX: Simple, responsive Bootstrap cards; clean layout with quantity input and Buy button.

Time Spent

Project Setup & Dockerization: ~1 hours

Django Models & Stripe Integration: ~3-4 hours

UI Design & Styling: ~30 hours
Testing & Debugging: ~1-2 hours
Total: ~7 hours

Notes / Recommendations:
Currently uses Stripe test mode; switch to live keys for production.
UI can be improved with images, modals, or a cart system.
Adding authentication per user allows persistent orders across sessions.
For production, use proper secrets management instead of .env in repo.
