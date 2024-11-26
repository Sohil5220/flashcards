from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a strong, unique key
CORS(app)  # Enable CORS for all origins

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flashcards.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    interval_hours = db.Column(db.Integer, default=1)  # Interval in hours
    next_review = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=1))

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "interval_hours": self.interval_hours,
            "next_review": self.next_review.isoformat(),
        }

# Create database tables
with app.app_context():
    db.create_all()


# Helper to find the closest card
def find_closest_card(excluded_id=None):
    now = datetime.utcnow()
    query = Flashcard.query.order_by(Flashcard.next_review.asc())
    if excluded_id is not None:
        query = query.filter(Flashcard.id != excluded_id)
    return query.first()

@app.route("/flashcards/review", methods=["GET"])
def get_flashcard_for_review():
    now = datetime.utcnow()
    last_reviewed_card_id = session.get("last_reviewed_card_id", None)

    # Find all cards eligible for review, excluding the last reviewed card
    eligible_cards = Flashcard.query.filter(Flashcard.next_review <= now)
    if last_reviewed_card_id:
        eligible_cards = eligible_cards.filter(Flashcard.id != last_reviewed_card_id)
    eligible_cards = eligible_cards.order_by(Flashcard.next_review.asc()).all()

    if eligible_cards:
        # Select the first eligible card
        card = eligible_cards[0]
        session["last_reviewed_card_id"] = card.id  # Update session with the current card ID
        return jsonify(card.to_dict())

    # If no eligible cards, find the card closest to the current time (excluding the last reviewed card)
    closest_card = find_closest_card(excluded_id=last_reviewed_card_id)
    if closest_card:
        session["last_reviewed_card_id"] = closest_card.id  # Update session with the current card ID
        return jsonify(closest_card.to_dict())

    # No flashcards available at all
    return jsonify({"message": "No flashcards available for review."}), 404


@app.route("/flashcards/<int:flashcard_id>", methods=["DELETE"])
def delete_flashcard(flashcard_id):
    flashcard = Flashcard.query.get(flashcard_id)
    if not flashcard:
        return jsonify({"message": "Flashcard not found"}), 404

    db.session.delete(flashcard)
    db.session.commit()
    return jsonify({"message": "Flashcard deleted successfully"})


# API to review a flashcard
@app.route("/flashcards/<int:card_id>/review", methods=["POST"])
def review_flashcard(card_id):
    data = request.json
    success = data.get("success")

    # Find the flashcard by ID
    card = Flashcard.query.get(card_id)
    if not card:
        return jsonify({"error": "Flashcard not found"}), 404

    now = datetime.utcnow()

    # Update `next_review` based on the result
    if success:
        # If the user remembered, increase the interval in hours
        card.interval_hours *= 2  # Double the interval on success
    else:
        # If the user forgot, reset to 1 hour
        card.interval_hours = 1

    # Update the next review time in hours
    card.next_review = now + timedelta(hours=card.interval_hours)
    db.session.commit()

    return jsonify({"message": "Review recorded", "next_review": card.next_review.isoformat()})

# API to create a new flashcard
@app.route("/flashcards", methods=["POST"])
def create_flashcard():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Question and answer are required"}), 400

    # Create a new flashcard
    flashcard = Flashcard(
        question=question,
        answer=answer,
        interval_hours=1,
        next_review=datetime.utcnow() + timedelta(hours=1)
    )
    db.session.add(flashcard)
    db.session.commit()

    return jsonify(flashcard.to_dict()), 201

# API to get all flashcards
@app.route("/flashcards", methods=["GET"])
def get_all_flashcards():
    flashcards = Flashcard.query.all()
    return jsonify([card.to_dict() for card in flashcards])

if __name__ == "__main__":
    app.run(debug = True)