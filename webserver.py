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


@app.route('/api/price_range', methods=['GET'])
def get_price_range():
    model = request.args.get('model')  # Get the car model from the query parameter
    if not model:
        return jsonify({"error": "Kindly put a valid model"}), 400

    try:
        query = """
         SELECT MIN(original_price), MAX(original_price)
         FROM cars
         WHERE model = %s
        """

        curr.execute(query, (model,))
        result = curr.fetchone()

        if result and result[0] is not None and result[1] is not None:
            return jsonify({
                "model": model,
                "min_price": result[0],
                "max_price": result[1]
            })
        else:
            return jsonify({"error": "No cars found for the given model"}), 404

    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True)