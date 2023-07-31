from flask import Flask, request, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy

obj = Flask(__name__)
DATABASE_NAME = 'reviews.db'
obj.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///reviews.db"
obj.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(obj)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(500), nullable=False)

@obj.route('/', methods=['POST', 'GET'])
def Home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        product_name = request.form['product']
        query = product_name.replace(" ", "-")
        url = f"https://www.amazon.in/{query}/product-reviews/B0BDHX8Z63/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
     
        for i,review in enumerate(reviews):
            product_name = product_name
            rating = float((review.find('a', {'data-hook': 'review-title'}).text)[:3])
            comments = (review.find('a', {'data-hook': 'review-title'}).text)[18:]
            name = review.find('div', {'class': 'a-profile-content'}).text
            obj = Reviews(id=i,product_name=product_name, rating=rating, comments=comments, name=name)
            db.session.add(obj)
            db.session.commit()
        
        allreview = Reviews.query.all()
        
        return render_template('display_reviews.html',allreview)

@obj.route('/display_reviews')
def display_reviews():
    reviews = Reviews.query.all()
    return render_template('display_reviews.html', reviews=reviews)

if __name__ == "__main__":
    db.create_all()  # Create the database tables
    obj.run()





