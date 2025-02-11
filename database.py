import psycopg2
from psycopg2 import sql

try:
    conn = psycopg2.connect(database = "Demo",
                            user = "postgres",
                            host = "localhost",
                            password = "1234",
                            port = 5432)

    curr = conn.cursor()
except Exception as error:
    print(f"An error occurred with the connection to the database: {error}")
    exit()

def check_table_exists():
    try:
        curr.execute("SELECT to_regclass('public.cars');")
        result = curr.fetchone()[0]

        if result:
            print("Table exists")
            return True
        else:
            return False

    except Exception as error:
        print(f"An error occurred while checking if table exists: {error}")

def create_table():
    try:

        if check_table_exists():        # If table already exists, move forward
            return

        # If table does not exist, create new table
        tableQuery = """
         CREATE TABLE IF NOT EXISTS cars(
         car_id SERIAL PRIMARY KEY,
         brand VARCHAR(100),
         model VARCHAR(100),
         year INT,
         status VARCHAR(50),
         color VARCHAR(50),
         transmission VARCHAR(50),
         discounted_price INT,
         original_price INT,
         url TEXT UNIQUE);
         """

        curr.execute(tableQuery)
        conn.commit()
        print("Table created successfully")

    except Exception as error:
        print(f"Error occurred on creating table: {error}")



def end_connection():
    curr.close()
    conn.close()



def insert_car(brand, model, year, status, color, transmission, discountedPrice, originalPrice, url):
    try:
        curr.execute("SELECT 1 FROM cars WHERE url = %s;", (url,))
        if curr.fetchone():
            return
        else:

            insertQuery = """
             INSERT INTO cars (
             brand,
             model,
             year,
             status,
             color,
             transmission,
             discounted_price,
             original_price,
             url)
             VALUES (
             %s,
             %s,
             %s,
             %s,
             %s,
             %s,
             %s,
             %s,
             %s);
             """

        curr.execute(insertQuery, (brand, model, year, status, color, transmission, discountedPrice, originalPrice, url))
        conn.commit()
        print(f"The car of brand {brand} and model {model} has been inserted")
    except Exception as error:
        print(f"Error occurred inserting new car: {error}")


create_table()