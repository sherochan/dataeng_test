from services.pghelper import pg_insert
from datetime import datetime

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

## to create sample data - temp 
def populate_db_temp():
    manufacturers = [
        {
            "name": "Honda"
        },
        {
            "name": "Toyota"
        },
        {
            "name": "Mercedes"
        },
        {
            "name": "Audi"
        }
    ]
    for manufacturer_dict in manufacturers:
        pg_insert("manufacturers", manufacturer_dict)

    cars = [
        {
            "manufacturer_id": 1,
            "model_name": "model name 11",
            "serial_number": "a172947920830294",
            "weight": 2700,
            "price": 100000.0
        },
        {
            "manufacturer_id": 1,
            "model_name": "model name 12",
            "serial_number": "a1729475020830294",
            "weight": 3100,
            "price": 90000.0
        },
        {
            "manufacturer_id": 1,
            "model_name": "model name 13",
            "serial_number": "a172947920130294",
            "weight": 1900,
            "price": 130700.0
        },
        {
            "manufacturer_id": 2,
            "model_name": "model name 21",
            "serial_number": "a27294792082224",
            "weight": 5000,
            "price": 170000.0
        },
        {
            "manufacturer_id": 2,
            "model_name": "model name 22",
            "serial_number": "a34294792082224",
            "weight": 3900,
            "price": 100000.0
        },
        {
            "manufacturer_id": 3,
            "model_name": "model name 31",
            "serial_number": "cs27294792082224",
            "weight": 1200,
            "price": 70000.0
        },
        {
            "manufacturer_id": 3,
            "model_name": "model name 32",
            "serial_number": "cs22224294792082224",
            "weight": 1900,
            "price": 80000.0
        },
        {
            "manufacturer_id": 4,
            "model_name": "model name 41",
            "serial_number": "z2729d4792082224",
            "weight": 3000,
            "price": 150000.0
        },
        {
            "manufacturer_id": 4,
            "model_name": "model name 42",
            "serial_number": "z2329d4792082224",
            "weight": 2800,
            "price": 200000.0
        },
        {
            "manufacturer_id": 4,
            "model_name": "model name 43",
            "serial_number": "z3r29d4792082224",
            "weight": 2710,
            "price": 123000.0
        }
    ]
    for car_dict in cars:
        pg_insert("cars", car_dict)

    salesmen = [
        {
            "first_name": "John",
            "last_name": "Lim",
            "phone" : "12345678",
            "date_joined": "2021-02-27"
        },
        {
            "first_name": "Harry",
            "last_name": "Tan",
            "phone" : "22345678",
            "date_joined": "2020-01-27"
        },
        {
            "first_name": "Tom",
            "last_name": "Toh",
            "phone" : "32345678",
            "date_joined": "2021-01-20"
        }
    ]
    for salesman_dict in salesmen:
        pg_insert("salesmen", salesman_dict)
    
    customer = [
        {
            "first_name": "customer guy 1",
            "last_name": "Lim",
            "phone": "987654321"   
        },
        {
            "first_name": "customer guy 2",
            "last_name": "Lim",
            "phone": "887654321"   
        },
        {
            "first_name": "customer guy 3",
            "last_name": "Lim",
            "phone": "787654321"   
        },
        {
            "first_name": "customer guy 4",
            "last_name": "Lim",
            "phone": "687654321"   
        }
    ]
    for customer_dict in customer:
        pg_insert("customers", customer_dict)
    

def get_timestamp_str():
    """
    Get current time in string 
    """
    now = datetime.now()
    timestamp_str = now.strftime(TIME_FORMAT)
    return timestamp_str

