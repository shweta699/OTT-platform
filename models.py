from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    youtube_url = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)  # Add this line
    rating = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
