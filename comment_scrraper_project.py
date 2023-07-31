from flask import Flask, request, render_template, redirect, url_for
import requests
from bs4 import BeautifulSoup
import pandas as pd

obj = Flask(__name__)

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
        
        product=[]
        rating=[]
        comments=[]
        name=[]
        for i,review in enumerate(reviews):
            product.append(product_name)
            rating.append(float((review.find('a', {'data-hook': 'review-title'}).text)[:3]))
            comments.append((review.find('a', {'data-hook': 'review-title'}).text)[18:])
            name.append(review.find('div', {'class': 'a-profile-content'}).text)
        table={"Product":product,"Custmer_Name":name,"Rating":rating,"Comments":comments}
        result=pd.DataFrame(table)

        try:
            existing_data_df = pd.read_excel('review.xlsx')
        except FileNotFoundError:
            existing_data_df = pd.DataFrame()

        appended_data_df = pd.concat([existing_data_df,result], ignore_index=True)


        with pd.ExcelWriter('review.xlsx', mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
            appended_data_df.to_excel(writer, index=False, sheet_name='Sheet1')

            
      
        
        



if __name__ == "__main__":
    obj.run()





