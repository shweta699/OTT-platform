from flask import Flask, render_template, request, redirect, url_for
from models import db, Movie, Review

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db.init_app(app)

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    return render_template('movie_detail.html', movie=movie, reviews=reviews)

@app.route('/add_review/<int:movie_id>', methods=['POST'])
def add_review(movie_id):
    rating = int(request.form['rating'])
    comment = request.form.get('comment')
    review = Review(movie_id=movie_id, rating=rating, comment=comment)
    db.session.add(review)
    
    movie = Movie.query.get_or_404(movie_id)
    movie.review_count += 1
    movie.rating = (movie.rating * (movie.review_count - 1) + rating) / movie.review_count
    db.session.commit()
    return redirect(url_for('movie_detail', movie_id=movie_id))

@app.route('/recommendations')
def recommendations():
    top_movies = Movie.query.order_by(Movie.rating.desc()).limit(5).all()
    return render_template('recommendations.html', movies=top_movies)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Sample data
        if not Movie.query.first():
            sample_movies = [
                Movie(
                    title='Inception',
                    description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.',
                    youtube_url='https://www.youtube.com/embed/YoHD9XEInc0',
                    image_url='https://m.media-amazon.com/images/I/51nbVEuw1HL._AC_SY679_.jpg'
                ),
                Movie(
                    title='The Matrix',
                    description='A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                    youtube_url='https://www.youtube.com/embed/vKQi3bBA1y8',
                    image_url='https://m.media-amazon.com/images/I/51EG732BV3L._AC_SY679_.jpg'
                ),
                Movie(
                    title='Interstellar',
                    description='A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                    youtube_url='https://www.youtube.com/embed/zSWdZVtXT7E',
                    image_url='https://m.media-amazon.com/images/I/91kFYg4fX3L._AC_SY679_.jpg'
                ),
                Movie(
                    title='The Dark Knight',
                    description='When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.',
                    youtube_url='https://www.youtube.com/embed/EXeTwQWrcwY',
                    image_url='https://m.media-amazon.com/images/I/71pox3zVs7L._AC_SY679_.jpg'
                ),
                Movie(
                    title='Forrest Gump',
                    description='The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.',
                    youtube_url='https://www.youtube.com/embed/bLvqoHBptjg',
                    image_url='https://m.media-amazon.com/images/I/61FhdEwhLmL._AC_SY679_.jpg'
                ),
                Movie(
                    title='Gladiator',
                    description='A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.',
                    youtube_url='https://www.youtube.com/embed/owK1qxDselE',
                    image_url='https://m.media-amazon.com/images/I/51AEB3EnnlL._AC_SY679_.jpg'
                ),
                Movie(
                    title='Titanic',
                    description='A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.',
                    youtube_url='https://www.youtube.com/embed/kVrqfYjkTdQ',
                    image_url='https://m.media-amazon.com/images/I/51FVG6I3ebL._AC_SY679_.jpg'
                ),
                Movie(
                    title='Jurassic Park',
                    description='A pragmatic Paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park\'s cloned dinosaurs to run loose.',
                    youtube_url='https://www.youtube.com/embed/QWBKEmWWL38',
                    image_url='https://m.media-amazon.com/images/I/71rNHGMVA7L._AC_SY679_.jpg'
                ),
                Movie(
                    title='Park',
                    description='A pragmatic Paleontologist visiting an almost complete theme park is tasked with protecting a couple of kids after a power failure causes the park\'s cloned dinosaurs to run loose.',
                    youtube_url='https://www.youtube.com/embed/QWBKEmWWL38',
                    image_url='https://m.media-amazon.com/images/I/71rNHGMVA7L._AC_SY679_.jpg'
                )
            ]
            db.session.bulk_save_objects(sample_movies)
            db.session.commit()

    app.run(debug=True)
