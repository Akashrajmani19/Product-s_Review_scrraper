from flask import Flask, request, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
obj = Flask(__name__)

@obj.route('/', methods=['POST', 'GET'])
def Home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        

        file_path = 'data.csv'
        if os.path.exists(file_path):
            os.remove(file_path)
   
        company = request.form['company']
        product= request.form['product']
        model= request.form['model']
        varient= request.form['varient']
        product_name=f"{company}-{product}-{model}-{varient}"
        url =f"https://www.amazon.in/{company}-{product}-{model}-{varient}/product-reviews/B0BMGB2TPR/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        reviews = soup.find_all('div', {'data-hook': 'review'})
        
        product=[]
        rating=[]
        comments=[]
        name=[]
        for i, review in enumerate(reviews):
            product.append(product_name)
            rating.append(float((review.find('a', {'data-hook': 'review-title'}).text)[:3]))
            comments.append((review.find('a', {'data-hook': 'review-title'}).text)[18:])
            name.append(review.find('div', {'class': 'a-profile-content'}).text)
        table = {"Product": product, "Customer_Name": name, "Rating": rating, "Comments": comments}
        result = pd.DataFrame(table)
        result.to_csv('data.csv', index=False)

        # Redirect to a new route to display the data
        return redirect(url_for('show_data'))

@obj.route('/show_data')
def show_data():
    data = pd.read_csv('data.csv')
    records = data.to_dict(orient='records')
    return render_template('display_reviews.html', records=records)

if __name__ == "__main__":
    obj.run(debug=True)





