import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd 
import datetime
from requests_html import HTMLSession
import yfinance as yf
import xlwings as xw

def web_content_div(web_content, class_path):
    web_content_div = web_content.findAll('div', class_path)
    try:
        spans = web_content_div[0].findAll('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts

def real_time_price(stock_code):
    url = ('https://in.finance.yahoo.com/quote/' + stock_code + '/history?p=' + stock_code )
    import yfinance as yf

    st = yf.Ticker(stock_code)
    hist = st.history(period="1y")
    hist_1 = st.history(period="6mo")
    one_ye = hist['Open'].values.tolist()[0]
    six_mo = hist_1['Open'].values.tolist()[0]
    try:
        r = requests.get(url)
        
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'D(ib) smartphone_Mb(10px) W(70%) W(100%)--mobp smartphone_Mt(6px)')
        
        if texts != []:
            price,change = texts[0], texts[1]
        else:
            price , change = [], []
        date_stamp = datetime.datetime.now()
        date_stamp = date_stamp.strftime('%Y-%m-%d')
        texts = web_content_div(web_content, 'Pb(10px) Ovx(a) W(100%)')
        
        if texts != []:
            for count, vol in enumerate(texts):
                high_list = []
                low_list = []
                for p in range(1,30):
                    high_list.append(texts[count+9+(7*p)])
                high = max(high_list)
                for p in range(1,30):
                    low_list.append(texts[count+10+(7*p)])
                low = min(low_list)
                break
        else:
            high = []
            low = []

    except ConnectionError:
        price , change, high, low, one_ye, six_mo = [], [], [], [], [], [], []

    return price, change,high, low, one_ye, six_mo

Stock = ['BTC-USD','XMR-USD','DOGE-USD','ADA-USD','DASH-USD','ETH-USD','MIOTA-USD','TRX-USD','EOS-USD','XLM-USD','DOT1-USD']

while (True):
    L = []
    col = []
    time_stamp = datetime.datetime.now()
    time_stamp = time_stamp.strftime('%Y-%m-%d %H:%M:%S')
    for stock_code in Stock:
        stock_price , change, high, low, one_ye, six_mo  = real_time_price(stock_code)
        info = []
        info.append(stock_price)
        info.extend([change])
        info.extend([high])
        info.extend([low])
        info.extend([one_ye])
        info.extend([six_mo])
        L.append(info)
    df = pd.DataFrame(L,columns = ['CP','PERC','HIGH(30d)','LOW(30d)', 'PRICE(1Y)', 'PRICE(6-mo)'], index = Stock)
    print('its working!')
    # df.to_excel('stock data.xlsx')
    wb = xw.Book('stock data.xlsx')
    sht1 = wb.sheets[0]
    sht1.range('B2:G2').value = L[0]
    sht1.range('B3:G3').value = L[1]
    sht1.range('B4:G4').value = L[2]
    sht1.range('B5:G5').value = L[3]
    sht1.range('B6:G6').value = L[4]
    sht1.range('B7:G7').value = L[5]
    sht1.range('B8:G8').value = L[6]
    sht1.range('B9:G9').value = L[7]
    sht1.range('B10:G10').value = L[8]
    sht1.range('B11:G11').value = L[9]
    sht1.range('B12:G12').value = L[10]
