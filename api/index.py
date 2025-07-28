# api/index.py
from flask import Flask, request, jsonify
from agent.vehicle_test_agent import VehicleTestAgent

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Vehicle Test Agent API is running!"})

@app.route("/run-tests", methods=["POST"])
def run_tests():
    try:
        # Initialize agent and run tests
        agent = VehicleTestAgent("data/dataset.csv")
        result = agent.run_all_tests()

        return jsonify({
            "status": "success",
            "report": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
