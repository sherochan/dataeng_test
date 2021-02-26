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
            id UUID PRIMARY KEY NOT NULL,
            name TEXT NOT NULL
        );
        """.format("manufacturers"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id UUID PRIMARY KEY NOT NULL,
            manufacturer_id UUID NOT NULL,
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
            id UUID PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone VARCHAR(15) NOT NULL,
            date_joined TIMESTAMP NOT NULL
        );
        """.format("salesmen"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id UUID PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone VARCHAR(15) NOT NULL
        );
        """.format("customers"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id UUID PRIMARY KEY NOT NULL,
            customer_id UUID NOT NULL,
            salesman_id UUID NOT NULL,
            transaction_date TIMESTAMP NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
            FOREIGN KEY (salesman_id) REFERENCES salesmen(id) ON DELETE CASCADE
        );
        """.format("transactions"),
        """
        CREATE TABLE IF NOT EXISTS {}
        (
            id UUID PRIMARY KEY NOT NULL,
            car_id UUID NOT NULL,
            transaction_id UUID NOT NULL,
            quantity INT NOT NULL,
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
    finally:
        if (connection):
            close_db_connection(connection, cursor)
        

