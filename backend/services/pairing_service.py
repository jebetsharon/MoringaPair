import random
from itertools import combinations
from backend.models import Pairing, Week, User, db

def _get_all_existing_pairs():
    """
    Returns a set of frozensets representing all existing student pairs ever created.
    This helps avoid repeated pairings until all combinations are exhausted.
    """
    existing_pairs = set()
    all_pairings = Pairing.query.all()
    for p in all_pairings:
        pair_set = frozenset([p.student_a_id, p.student_b_id]) if p.student_b_id else frozenset([p.student_a_id])
        existing_pairs.add(pair_set)
    return existing_pairs

def _generate_unique_pairs(student_ids):
    """
    Generate unique pairs for the week such that no previous pairs are repeated
    until all possible pairs are exhausted.
    """
    existing = _get_all_existing_pairs()
    all_possible_pairs = list(combinations(student_ids, 2))
    random.shuffle(all_possible_pairs)

    pairs = []
    used_students = set()

    # Try to find pairs that don't exist yet
    for a, b in all_possible_pairs:
        pair_set = frozenset((a, b))
        if pair_set not in existing and a not in used_students and b not in used_students:
            pairs.append((a, b))
            used_students.update([a, b])
            existing.add(pair_set)

    # Handle unpaired student if odd count
    unpaired_students = set(student_ids) - used_students
    if unpaired_students:
        unpaired = unpaired_students.pop()
        pairs.append((unpaired, None))

    # If all pairs already exist, allow repeats but avoid pairing a student twice in this week
    if len(used_students) < len(student_ids):
        remaining_students = set(student_ids) - used_students
        available_students = list(used_students)
        for student in remaining_students:
            if available_students:
                partner = available_students.pop()
                pairs.append((student, partner))
            else:
                # No one left to pair, lone student
                pairs.append((student, None))

    return pairs

def create_pairings_for_new_week(description="Auto generated"):
    """
    Creates pairings for a new week.
    """
    students = User.query.filter_by(role="student").all()
    student_ids = [s.id for s in students]

    if not student_ids:
        raise Exception("No students available for pairing")

    latest_week_num = db.session.query(db.func.max(Week.week_number)).scalar() or 0
    week = Week(week_number=latest_week_num + 1, description=description, published=True)
    db.session.add(week)
    db.session.flush()  # get week.id without commit

    try:
        pairs = _generate_unique_pairs(student_ids)
        for a_id, b_id in pairs:
            pairing = Pairing(student_a_id=a_id, student_b_id=b_id, week_id=week.id)
            db.session.add(pairing)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Failed to create pairings: {str(e)}")

    return week

def get_current_pairing_for_user(user_id):
    """
    Returns the pairing and the week for the latest week for the given user.
    """
    latest_week = Week.query.order_by(Week.week_number.desc()).first()
    if not latest_week:
        return None, None

    pairing = Pairing.query.filter(
        Pairing.week_id == latest_week.id,
        ((Pairing.student_a_id == user_id) | (Pairing.student_b_id == user_id))
    ).first()
    return pairing, latest_week
