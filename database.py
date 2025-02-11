import psycopg2

TABLE_QUERY = """
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

INSERT_QUERY = """
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

URL_QUERY = """
          SELECT url
          FROM cars
          """

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
        curr.execute(TABLE_QUERY)
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

        curr.execute(INSERT_QUERY, (brand, model, year, status, color, transmission, discountedPrice, originalPrice, url))
        conn.commit()
        print(f"The car of brand {brand} and model {model} has been inserted")
    except Exception as error:
        print(f"Error occurred inserting new car: {error}")


def get_url_links():
    try:
        curr.execute(URL_QUERY)
    except Exception as error:
        print(f"Error occurred during compilation of url links: {error}")

create_table()