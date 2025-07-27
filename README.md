# MORINGA PAIR

Moringa Pair is a backend application designed to manage weekly pairing, feedback, and quizzes for students in a learning environment. Built using Flask, SQLAlchemy, and PostgreSQL, this system helps automate and track academic progress and peer interaction efficiently.

---

# ## 👥 Contributors

This project was collaboratively built by a team of Moringa students, each contributing to key components of the backend system:

- **Sharon** – Implemented user profile management and JWT-based authentication.
- **Louis** – Developed partner pairing logic and partner-related API routes.
- **Jesse** – Handled weekly pairing system and implemented week-based endpoints.
- **Rohan** – Built the quiz results system and feedback submission/retrieval functionality.


## 🛠 Tech Stack

- **Backend**: Flask (RESTful API)
- **Database**: PostgreSQL (via SQLAlchemy ORM)
- **Migrations**: Flask-Migrate
- **Authentication**: JWT (JSON Web Tokens)
- **Environment Management**: `python-dotenv`

---

## 🚀 Features

- **User Roles**: Students and Admins
- **Authentication**: Login via JWT
- **Weekly Quizzes**: Create, Submit, and Retrieve
- **Peer Feedback**: Anonymous or public feedback between users
- **CI/CD Ready**: GitHub integration enabled
- **Custom Error Handling**: Unified error responses with status codes
- **Pagination**: For large feedback or quiz datasets
- **Environment Configuration**: `.env` usage for secure settings

---

## ✅ Setup Instructions

1. **Clone the repo**

```bash
git clone < https/ssh url >
cd backend
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Set up environment variables

Create a .env file at the root:

ini
Copy
Edit
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://moringa_user:moringa123@localhost:5432/moringa_pair_db
Run migrations

bash
Copy
Edit
flask db init
flask db migrate
flask db upgrade
Run the app

bash
Copy
Edit
flask run
🔐 Authentication & Route Protection
JWT is used for secure authentication.

Protected routes require a valid token.

Role-based access ensures only admins access certain features.

🧪 Testing
You can use tools like Postman or cURL to test the API routes:

Example: Login to get token
bash
Copy
Edit
POST /login
{
  "email": "student@example.com",
  "password": "password123"
}
Use token in protected routes
Add this to your headers:

makefile
Copy
Edit
Authorization: Bearer <your_token>
📄 Important Commands
Task	Command
Activate venv	source venv/bin/activate
Run server	flask run
DB migration	flask db migrate -m "message"
Apply migration	flask db upgrade

👥 Contributors
This project was collaboratively built by Sharon, Rohan, Louis and Jesse as part of a backend module assessment. Each member contributed through clearly defined ClickUp tasks, pull requests, and code reviews.

📌 Notes
All API routes return standardized JSON responses.

Pull requests are reviewed before merging into main.
// trigger rebuild
