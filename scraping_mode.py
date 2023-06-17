from requests import Session 
from .calculation import DataSaver
from array import array
from time import sleep
 
FEATCH = Session().get 

API = 'https://www.nseindia.com/api/option-chain-indices?symbol='

Symbol = ("NIFTY","FINNIFTY","BANKNIFTY");

Headers = {
    'authority': 'www.nseindia.com',
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9',
    'referer': 'https://www.nseindia.com/option-chain',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'content-type': 'application/json'
}

def find_closest_value(number, value_list):
    closest_value = None
    min_difference = float('inf')
    for value in value_list:
        difference = abs(value - number)
        if difference < min_difference:
            min_difference = difference
            closest_value = value
    return closest_value

get_table_data_json_format = lambda n : FEATCH(API+n,headers=Headers).json();

def data_cleaning(table_session,range_=500,date=None):
    out_put = []
    # table_session = get_table_data_json_format(Symbol[n])
    timestamp = table_session['records']["timestamp"];
    index_price = (table_session["records"]["underlyingValue"])
    table_data =  table_session["filtered"]["data"];

    StrikePrices = array('i',range(table_data[0]["strikePrice"],table_session["records"]["strikePrices"][-1],50));
    
    if(len(StrikePrices)<(range_/50)):range_ = 100;
    
    close_price = (find_closest_value(index_price,StrikePrices))
    starting =  (close_price) - range_;
    ending =    (close_price) + range_;
    
    final_range = array('i',range(starting,ending+1,50));
    
    for i in table_data:
        if not date:
            if i['CE']["strikePrice"] in final_range:       
                PUT_IO = (i['PE']['openInterest'])
                PUT_C_IO = (i['PE']['changeinOpenInterest'])
                CALL_IO  = (i['CE']['openInterest'])
                CALL_C_IO = (i['CE']['changeinOpenInterest'])
                StrikePrices_ = i['CE']["strikePrice"]
                out_put.append(DataSaver(StrikePrices_,PUT_IO,CALL_IO,PUT_C_IO, CALL_C_IO));
    return out_put


def date_data_cleaning(table_session,date=None):
    range_ = 500;
    out_put  = [];
    table_data = table_session["records"]["data"]
    
    index_price = table_data[0]['CE']['underlyingValue'];
    print(index_price)
    
    StrikePrices = array('i',range(table_data[0]["strikePrice"],table_session["records"]["strikePrices"][-1],50));

    if(len(StrikePrices)<(500/50)):range_ = 100;
    
    close_price = (find_closest_value(index_price,StrikePrices))
    starting =  (close_price) - range_;
    ending =    (close_price) + range_;
    final_range = array('i',range(starting,ending+1,50));
    # print(index_price)
    for i in table_data:
        if i.get('CE') is not None:
                if i['CE']["strikePrice"] in final_range and i['CE']["expiryDate"] == date:
                    PUT_IO = (i['PE']['openInterest'])
                    PUT_C_IO = (i['PE']['changeinOpenInterest'])
                    CALL_IO  = (i['CE']['openInterest'])
                    CALL_C_IO = (i['CE']['changeinOpenInterest'])
                    StrikePrices_ = i['CE']["strikePrice"]
                    out_put.append(DataSaver(StrikePrices_,PUT_IO,CALL_IO,PUT_C_IO, CALL_C_IO));
    return out_put


# print(data_cleaning(1-1,range_=500,date="29-Jun-2023"))
# table_session = get_table_data_json_format(Symbol[0])
# print(date_data_cleaning(table_session,"29-Jun-2023"))

    
    