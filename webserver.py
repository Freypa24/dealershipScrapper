from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)


try:
    conn = psycopg2.connect(database = "Demo",
                            user = "postgres",
                            host = "localhost",
                            password = "1234",
                            port = 5432)

    curr = conn.cursor()
except Exception as error:
    print(f"There was an error with the connection to the database: {error}")
    exit()


def convert_integer_price(num):
    return " P {:,.2f}".format(num)


@app.route('/api/price_range', methods=['GET'])
def get_price_range():
    model = request.args.get('model')
    if not model:
        return jsonify({"error": "Kindly put a valid model"}), 400

    try:
        query = """
         SELECT MIN(original_price), MAX(original_price), AVG(original_price)
         FROM cars
         WHERE model = %s
        """

        curr.execute(query, (model,))
        result = curr.fetchone()

        if result and result[0] is not None and result[1] is not None and result[2] is not None:

            return jsonify({
                "Car Model": model,
                "Min Price": convert_integer_price(result[0]),
                "Max Price": convert_integer_price(result[1]),
                "Average Price": convert_integer_price(result[2])
            })
        else:
            return jsonify({"error": "No cars found for the given model. Try capitalizing the first letter?"}), 404

    except Exception as error:
        return jsonify({"error": str(error)}), 500


## SPACE FOR FURTHER API CALLS

if __name__ == '__main__':
    app.run(debug=True)