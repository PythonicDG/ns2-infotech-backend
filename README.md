# NS2 Infotech Backend

The backend server for NS2 Infotech, built with Django and Django REST Framework.

## Features
- Scalable Django architecture
- REST APIs for homepage, services, training, and more
- PostgreSQL integration
- Continuous Deployment ready (Railway)

## Tech Stack
- **Framework:** Django 5.2.5
- **API:** Django REST Framework
- **Database:** PostgreSQL
- **Server:** Gunicorn / Hypercorn
- **Static Files:** WhiteNoise

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ns2-infotech-backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and fill in the details.

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the server:**
   ```bash
   python manage.py runserver
   ```

## Deployment
The project is configured for deployment on Railway using the provided `railway.toml` and `Procfile`.

## Contribution
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License
Distributed under the MIT License.
