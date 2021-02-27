from flask import Flask, request, jsonify
from services.pghelper import (
    create_tables,
    pg_get_row_by_col,
    pg_insert,
    pg_get_col,
    pg_get_customer_spending
)
from utils.utils import (
    populate_db_temp,
    get_timestamp_str
)

import uuid, logging

app = Flask(__name__)

@app.route('/v1',  methods = ["GET"])
def main():
    return {"status": "success", "message": "dataeng_test Q2"}

@app.route('/v1/get_Q2_1',  methods = ["GET"])
def get_Q2_1():
    """
    for qns 2 part 1
    """
    message_json = {
        "status": "incomplete",
        "results": []
    }
    results, err = pg_get_customer_spending()
    columns_lst = ["customer_id","first_name","last_name","total_spending"]
    if err is None:
        for result in results:
            result_dict = dict(zip(columns_lst, result))
            result_total_spending = "0"
            if result_dict["total_spending"] is not None:
                result_total_spending = str(result_dict["total_spending"])
            result_dict["total_spending"] = result_total_spending
            message_json["results"].append(result_dict)
        message_json["status"] = "complete"
    else:
        message_json["error"] = err
    
    return jsonify(message_json)


@app.route('/v1/db_populate',  methods = ["POST"])
def auto_populate_db():
    """
    populate the database with sample data 

    Returns:
    --------
    json in the form of 
        {
            "status": "completed"
        } # if no error 
        OR 
        {
            "status": "incomplete,
            "error": .... 
        }
    """
    message_json = {
        "status": "incomplete"
    }
    try:
        populate_db_temp()
    except Exception as e:
        message_json["error"] = str(e)
    else:
        message_json["status"] = "complete"
    finally:
        return jsonify(message_json)


@app.route('/v1/make_transaction',  methods = ["POST"])
def make_transaction():
    """
    Create a transaction 
    NOTE: Assume phone number is unique for each customer 
    
    example of request body :
    {
        "customer_first_name" : john,
        "customer_last_name" : doe,
        "phone": "12345678",
        "salesman_id" : ...,
        "car_id" : ..,
        "quantity" : 1
    }
    Returns:
    --------
    json in the form of 
        {
            "status": "completed"
        } # if no error 
        OR 
        {
            "status": "incomplete,
            "error": .... 
        }
    """
    message_json = {
        "status": "incomplete"
    }
    try:
        # first update customer table 
        customer_row_info = pg_get_row_by_col("customers","phone", request.json["phone"])
        print("customer row info print= {}".format(customer_row_info))
        logging.info("customer row info log= {}".format(customer_row_info))
        if customer_row_info is None: # is none 
            # customer do not exist
            customer_status = {
                "first_name": request.json["customer_first_name"],
                "last_name": request.json["customer_last_name"],
                "phone": request.json["phone"]
            }
            pg_insert("customers", customer_status)
            customer_row_info = pg_get_row_by_col("customers","phone", request.json["phone"])
        
        # get customer id 
        print("customer row info print 2= {}".format(customer_row_info))
        logging.info("customer row info log 2= {}".format(customer_row_info))
        columns_lst = pg_get_col("customers")
        print("customer list print 3= {}".format(columns_lst))
        customer_row_dict = dict(zip(columns_lst, customer_row_info))
        # print("customer row dict print 3= {}".format(customer_row_dict))
        customer_id = customer_row_dict["id"]

        transaction_uuid = uuid.uuid1()
        transaction_status = {
            "id": str(transaction_uuid),
            "customer_id": customer_id,
            "salesman_id": request.json["salesman_id"],
            "transaction_date": get_timestamp_str()
        }
        pg_insert("transactions", transaction_status)
        print("transaction status = {}".format(transaction_status))

        transaction_details_status = {
            "car_id": request.json["car_id"],
            "transaction_id": str(transaction_uuid),
            "quantity": request.json["quantity"]
        }

        pg_insert("transaction_details", transaction_details_status)
        print("transaction details status = {}".format(transaction_details_status))
    except Exception as e:
        message_json["error"] = str(e)
    else:
        message_json["status"] = "completed"
    finally:
        return jsonify(message_json)


if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", debug=True)