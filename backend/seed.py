import random
from faker import Faker
from datetime import datetime, timedelta
from backend.app import create_app
from backend.models import User, Week, Pairing,db
from werkzeug.security import generate_password_hash

fake = Faker()
app = create_app()

with app.app_context():
    print("Connected to PostgreSQL DB:", db.engine.url)
    
def seed_users(n=10):
    print("Seeding users...")
    users = []
    for _ in range(n):
        full_name = fake.name()
        email = fake.unique.email()
        password_hash = generate_password_hash("password123")
        role = random.choice(["student", "admin"])

        user = User(full_name=full_name, email=email, password_hash=password_hash, role=role)
        db.session.add(user)
        users.append(user)

    db.session.commit()
    return users

def seed_weeks(n=5):
    print("Seeding weeks...")
    weeks = []
    start_date = datetime.today()
    for i in range(n):
        week = Week(
            week_number=i + 1,
            start_date=start_date + timedelta(weeks=i),
            end_date=start_date + timedelta(weeks=i+1) - timedelta(days=1),
            description=f"Week {i + 1} overview",
            published=random.choice([True, False])
        )
        db.session.add(week)
        weeks.append(week)

    db.session.commit()
    return weeks

def seed_pairings(users, weeks, n=10):
    print("Seeding pairings...")
    pairings = []
    for _ in range(n):
        student_a, student_b = random.sample(users, 2)
        week = random.choice(weeks)

       
        if student_a.id != student_b.id:
            pairing = Pairing(
                student_a_id=student_a.id,
                student_b_id=student_b.id,
                week_id=week.id
            )
            db.session.add(pairing)
            pairings.append(pairing)

    db.session.commit()
    return pairings

def run_seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = seed_users(15)
        weeks = seed_weeks(6)
        seed_pairings(users, weeks, 20)

        print("✅ Seeding completed.")

if __name__ == "__main__":
    run_seed()
