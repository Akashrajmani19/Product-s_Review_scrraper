from flask import Flask,request,render_template
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen



obj = Flask(__name__)

@obj.route('/', methods = [POST,GET])
def Home():
    if request.method=="GET":
        return render_template("index.html")
    else:
        product_name=request.form['product']
        query = product_name.replace(" ","-")
        url =f"https://www.amazon.in/{query}/product-reviews/B0BDHX8Z63/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
        
        response = requests.get(url)
        Soup = BeautifulSoup(response.content,"html.parser")
        reviws = Soup.find_all('div',{'data-hook':'review'})
        rating = []
    comments=[]
    name=[]
    product_name=[]
    for i in reviws:
        product_name.append(product_name)
        rating.append(float((i.find('a',{'data-hook':'review-title'}).text)[:3]))
        comments.append((i.find('a',{'data-hook':'review-title'}).text)[18:])
        name.append(i.find('div',{'class':'a-profile-content'}).text)



