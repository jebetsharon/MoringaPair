from backend.models import db, QuizResult, User, Pairing, Week
from sqlalchemy.sql import func


def save_quiz_result(user_id, score, strength, weakness):
    if not (0 <= score <= 100):
        raise ValueError("Score must be between 0 and 100.")

    qr = QuizResult.query.filter_by(user_id=user_id).first()
    if not qr:
        qr = QuizResult(user_id=user_id, score=score, strength_area=strength, weakness_area=weakness)
        db.session.add(qr)
    else:
        qr.score = score
        qr.strength_area = strength
        qr.weakness_area = weakness

    try:
        db.session.commit()
        auto_pair_users()  # Automatically try pairing after each submission
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Failed to save quiz result: {str(e)}")

    return qr


def get_quiz_result(user_id):
    return QuizResult.query.filter_by(user_id=user_id).first()


def auto_pair_users():
    paired_ids = set()
    all_results = QuizResult.query.all()

    # Clear existing pairs before pairing anew
    Pairing.query.delete()
    db.session.commit()

    latest_week = Week.query.order_by(Week.week_number.desc()).first()
    if not latest_week:
        raise Exception("No active week found to assign pairing.")

    for i in range(len(all_results)):
        user_a = all_results[i]
        if user_a.user_id in paired_ids:
            continue

        closest = None
        closest_diff = 100  # max possible diff

        for j in range(i + 1, len(all_results)):
            user_b = all_results[j]
            if user_b.user_id in paired_ids:
                continue

            diff = abs(user_a.score - user_b.score)
            if diff < closest_diff:
                closest = user_b
                closest_diff = diff

        if closest:
            new_pair = Pairing(
                student_a_id=user_a.user_id,
                student_b_id=closest.user_id,
                week_id=latest_week.id
            )
            db.session.add(new_pair)
            paired_ids.add(user_a.user_id)
            paired_ids.add(closest.user_id)

    db.session.commit()
