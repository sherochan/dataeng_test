import psycopg2

import logging

from config import configs

def create_db_connection():
    try:
        connection = psycopg2.connect(**configs["postgres"])
        cursor = connection.cursor()
    except (Exception, psycopg2.DatabaseError) as error :
        print("error while connecting = {}".format(error))
        logging.info("Error while connecting: {}".format(error))
    else:
        return connection, cursor

def close_db_connection(connection, cursor):
    cursor.close()
    connection.close()

def create_tables():
    """
    to create all the necessary tables as per stated in the ERD
    """
    sql_queries = [
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id SERIAL PRIMARY KEY NOT NULL,
            name TEXT NOT NULL
        );
        """.format("manufacturers"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id SERIAL PRIMARY KEY NOT NULL,
            manufacturer_id INT NOT NULL,
            model_name TEXT NOT NULL,
            serial_number TEXT NOT NULL,
            weight INT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id) ON DELETE CASCADE
        );
        """.format("cars"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id SERIAL PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone VARCHAR(15) NOT NULL,
            date_joined TIMESTAMP NOT NULL
        );
        """.format("salesmen"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id SERIAL PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone VARCHAR(15) NOT NULL
        );
        """.format("customers"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id UUID PRIMARY KEY NOT NULL,
            customer_id INT NOT NULL,
            salesman_id INT NOT NULL,
            transaction_date TIMESTAMP NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
            FOREIGN KEY (salesman_id) REFERENCES salesmen(id) ON DELETE CASCADE
        );
        """.format("transactions"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            car_id INT NOT NULL,
            transaction_id UUID NOT NULL,
            quantity INT NOT NULL,
            PRIMARY KEY (car_id, transaction_id),
            FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
        );
        """.format("transaction_details")

    ]
    try:
        connection, cursor = create_db_connection()
        for sql_create_query in sql_queries:
            cursor.execute(sql_create_query)
        connection.commit()
    except Exception as e:
        print("error creating tables : {}".format(e))
        logging.info("error creating tables : {}".format(e))
        raise
    finally:
        if (connection):
            close_db_connection(connection, cursor)
        

def pg_insert(table_name, status):
    """
    insert a single row into the given table_name 

    Params:
    -------
    table_name: string
    status: dictionary of variable size, key-value pair of which key = column_name,
        value = the corresponding value for the column
    
    Returns:
    --------
    None
    """
    print("status = {}".format(status))
    err = None
    try:
        connection, cursor = create_db_connection()
        columns_lst = list(status.keys())
        values_tup = tuple(status.values())

        columns_str = ", ".join(columns_lst)
        values_str = ", ".join(["%s "] * len(columns_lst))
        print("values _str = {}".format(values_str))
        sql_query = """
            INSERT INTO {}({})
            VALUES({});
        """.format(table_name, columns_str, values_str)
        print("sql query!! = {}".format(sql_query))
        cursor.execute(sql_query, values_tup)
        connection.commit()
    except Exception as e:
        error_message = "error in inserting a single row ={}".format(e)
        logging.info(error_message)
        err = error_message
    else:
        if (connection):
            close_db_connection(connection, cursor)
        return err
    
def pg_update_id(table_name, _id, status):
    """
    given id and tablename, 
        update row in the given table for that id w the new details
    
    Params:
    -------
    table_name: string
    _id: string
    status: dictionary of variable size, key-value pair of which key = column_name,
        value = the corresponding value for the column
    
    Returns:
    --------
    None or error message
    """
    print("status = {}".format(status))
    err= None
    try:
        connection, cursor = create_db_connection()
        columns_lst = list(status.keys())
        values_tup = tuple(status.values())

        columns_str = ", ".join(columns_lst)

        sql_query = """
            UPDATE {}
            SET ({})=%s
            WHERE id='{}';
        """.format(table_name, columns_str, _id)

        multiple_values = (values_tup, )
        cursor.execute(sql_query, multiple_values)
        connection.commit()
    except Exception as e:
        error_message = "error in updating db = {}".format(e)
        logging.info(error_message)
        err = error_message
    finally:
        if (connection):
            close_db_connection(connection, cursor)
        return err

def pg_get_id(table_name, _id):
    """
    given table_name and id, get the row that satisfy this condition

    Params:
    -------
    table_name: string
    _id: string 

    Returns:
    --------
    a tuple of values if exist
    """
    res = None 
    try:
        connection, cursor = create_db_connection()
        sql_query = """
            SELECT * FROM {}
            WHERE id = '{}';
        """.format(table_name, _id)
        cursor.execute(sql_query)
        res = cursor.fetchone()
    except Exception as e:
        print("error in getting row = {}".format(e))
        raise
    finally:
        if (connection):
            close_db_connection(connection, cursor)
        return res

def pg_get_row_by_col(table_name, col_name, col_value):
    """
    given a column name and col_value , find ONE row 
        in the specified table which this condition fulfil

    Params:
    -------
    table_name: string
    col_name: string
    col_value: int/string/float

    Returns:
    --------
    None if dun exist OR 
        a tuple with the values 
    """
    res = None 
    try:
        connection, cursor = create_db_connection()
        values_tup = (col_value,)
        sql_query = """
            SELECT * FROM {}
            WHERE ({})= %s ;
        """.format(table_name, col_name)
        print("sql_query retrieve condition = {}".format(sql_query))
        logging.info("sql_query retrieve condition log = {}".format(sql_query))
        cursor.execute(sql_query, values_tup)
        res = cursor.fetchone()
        print("res = {}".format(res))
    except Exception as e:
        print("error in retrieving a row by col conditions = {}".format(e))
        raise
    finally:
        if (connection):
            close_db_connection(connection, cursor)
        return res

def pg_get_col(table_name):
    """
    get column names belonging to the specified table 

    Params:
    -------
    table_name: string 

    Returns:
    --------
    a list of column names 
    """
    res = None
    try:
        connection, cursor = create_db_connection()
        sql_query = """
            SELECT * FROM {} LIMIT 0;
        """.format(table_name)
        cursor.execute(sql_query)
        res = [column.name for column in cursor.description]
    
    except Exception as e:
        print("error in getting column names = {}".format(e))
        raise
    finally:
        if (connection):
            close_db_connection(connection, cursor)
        return res
    
def pg_delete_id(table_name, _id):
    """
    delete row with given id in the specified table 

    Params:
    -------
    table_name: string
    _id: string 

    Returns:
    --------
    None
    """
    try:
        connection, cursor = create_db_connection()
        sql_query = """
            DELETE FROM {}
            WHERE id = '{}';
        """.format(table_name, _id)
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        print("error in deleting row = {}".format(e))
        raise
    finally:
        if (connection):
            close_db_connection(connection, cursor)


##### Q2.1
def pg_get_customer_spending():
    """
    to address Qns 2 part 1 - I want to know the list of our customers and their spending.
    """
    err = None
    try:
        connection, cursor = create_db_connection()
        # sql_query = """
        # SELECT id as transaction_id, customer_id
        # FROM transactions 
        # WHERE transactions.customer_id in (
        #     SELECT id as customer_id
        #     FROM customers
        # )
        # """
        sql_query = """
            SELECT customers.id, customers.first_name, customers.last_name, transaction_customer_info.total_spending
            FROM customers
            LEFT JOIN
            (
                SELECT count(transactions.id) as transaction_counts, transactions.customer_id as customer_id,  SUM(car_transaction_details.quantity), SUM(car_transaction_details.price * car_transaction_details.quantity) AS total_spending
                FROM transactions
                LEFT JOIN
                (
                    SELECT cars.id as car_id, cars.price, transaction_details.quantity, transaction_details.transaction_id
                    FROM cars
                    RIGHT JOIN
                    transaction_details
                    ON (cars.id = transaction_details.car_id)
                ) as car_transaction_details
                ON (transactions.id = car_transaction_details.transaction_id)
                GROUP BY customer_id
            ) as transaction_customer_info
            ON transaction_customer_info.customer_id = customers.id
        
            ;

        """
        cursor.execute(sql_query)
        results = cursor.fetchall()
    except Exception as e:
        error_message = "error in deleting row = {}".format(e)
        err = error_message
        
    finally:
        if (connection):
            close_db_connection(connection, cursor)
        return results, err

    
