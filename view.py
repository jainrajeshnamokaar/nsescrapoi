
from flask import render_template,Blueprint,jsonify
from .scraping_mode import Symbol,get_table_data_json_format,data_cleaning
# from flask_caching import Cache
from . import cache
# from requests import get 


views = Blueprint("views",__name__);

@views.route('/')
@views.route("/home")
def home():
    return render_template("home.html",symbol=Symbol);

@views.route('/ExpiryDate/<n>')
@cache.cached(timeout=3600)
def expiry_date(n):
    options_data = cache.get(n)
    if options_data is not None:
        return jsonify(options_data)
    else:
        rsponce = get_table_data_json_format(n)
        options_data_exp_date = rsponce['records']['expiryDates'];
        value_to_display = data_cleaning(rsponce)
        
        display_data = ([{"strike_price":x.strike_price ,"put_io":x.put_io,"call_io":x.call_io,
                "put_change_io":x.put_change_io,"call_change_io":x.call_change_io} for x in value_to_display])
        
        cache.set(f"{n}_object_1",value_to_display)
        
        cache.set(n, [options_data_exp_date,display_data])
        
        return jsonify(cache.get(n))


@views.route("/update_data/<n>")
def update_data(n):
    
    options_data_of_old_one = cache.get(n+"_object_1");
    
    if options_data_of_old_one is not None:
        new_rsponce = get_table_data_json_format(n)
        class_object = data_cleaning(new_rsponce);
        # print(class_object)
        send_value = (list(map(lambda n:n[0]%n[1],list(zip(options_data_of_old_one,class_object)))))
        send_value = [item[0] for item in send_value]
        # cache.delete(n+"_object_1")
        cache.set(n+"_object_1",class_object);
        
        return jsonify(send_value);
        
    return "";
