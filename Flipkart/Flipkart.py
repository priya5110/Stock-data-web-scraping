from bs4 import BeautifulSoup  
import requests 
import pandas as pd

page_num = input("Enter the number of pages you want to Scrap: ")  #total pages = 6
device_name = []
device_price = []
device_rating = []
for i in range(1,int(page_num)+1):
    url = r"https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3Drealme&p%5B%5D=facets.availability%255B%255D%3DExclude%2BOut%2Bof%2BStock&param=7564&otracker=clp_metro_expandable_1_3.metroExpandable.METRO_EXPANDABLE_Shop%2BNow_mobile-phones-store_Q1PDG4YW86MF_wp3&fm=neo%2Fmerchandising&iid=M_f9b6e9c4-1799-4f4b-b4df-e7c1639fd941_3.Q1PDG4YW86MF&ppt=hp&ppn=homepage&ssid=gw1wegxiww0000001639057617335&page=" + str(i)
    req = requests.get(url)
    content = BeautifulSoup(req.content,'html.parser')
    name = content.find_all('div', {"class":"_4rR01T"})
    price = content.find_all('div', {"class":"_30jeq3 _1_WHN1"})
    rating = content.find_all('div', {"class":"_3LWZlK"})
    
    for i in name:
        device_name.append(i.text)
    for i in price:
        device_price.append(i.text[1:]) 
    for i in rating:
        device_rating.append(i.text)
print(len(device_price),len(device_rating),len(device_name))
data = {"Name": device_name, "Price (in Rs)": device_price, "Rating":device_rating}
df = pd.DataFrame(data)
print(df)
df.to_csv('data.csv')