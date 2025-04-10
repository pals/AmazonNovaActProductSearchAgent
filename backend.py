from flask import Flask, request, jsonify, render_template
import subprocess
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)


def run_search_script(product_name: str) -> list:
    """Runs the nova-script.py and returns the parsed product data."""
    logger.info(f"Running nova-script.py with product_name: '{product_name}'")
    try:
        result = subprocess.run(
            ["python3", "nova-script.py", product_name],
            capture_output=True,
            text=True,
            check=True,
        )
        logger.info(f"nova-script.py completed with exit code: 0")
        logger.debug(f"nova-script.py stdout:\n{result.stdout}")

        output_str = result.stdout.strip()
        try:
            # Load the JSON output from nova-script.py
            product_data = json.loads(output_str)
            logger.debug(f"Parsed JSON output: {product_data}")
            return product_data
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}\nOutput: {output_str}")
            return [{"error": "Error decoding JSON from search script"}]

    except subprocess.CalledProcessError as e:
        logger.error(
            f"Error running nova-script.py: {e}\nStderr: {e.stderr}\nStdout: {e.stdout}"
        )
        return [{"error": f"Error running search script: {e}"}]
    except FileNotFoundError:
        logger.error("Error: nova-script.py not found.")
        return [{"error": "Error: nova-script.py not found."}]


@app.route("/")
def index():
    logger.info("Serving index.html")
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    logger.info("Received /search request")
    data = request.get_json()
    logger.debug(f"Request data: {data}")
    product_name = data.get("product_name")
    if product_name:
        search_results = run_search_script(product_name)
        logger.info(f"Returning search results: {search_results}")
        return jsonify(search_results)
    else:
        logger.warning("Product name not provided in /search request.")
        return jsonify({"error": "Product name not provided."}), 400


if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True)