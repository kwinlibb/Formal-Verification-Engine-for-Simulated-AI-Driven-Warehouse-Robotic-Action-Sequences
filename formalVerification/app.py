from flask import Flask, request, jsonify
from flask_cors import CORS
from pyswip import Prolog

app = Flask(__name__)
CORS(app)

prolog = Prolog()
prolog.consult("rules.pl")

@app.route("/", methods=["GET"])
def home():
    return "Formal Verification Server is running"

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    actions_raw = data["actions"]

    # Convert "[A, B, C]" into ['A','B','C']
    actions = [a.strip() for a in actions_raw.strip("[]").split(",")]

    results = []
    all_valid = True

    for action in actions:
        q = f"validate({action.lower()}, Result)."
        res_list = list(prolog.query(q))

        if res_list:
            result = res_list[0]["Result"]
        else:
            result = "invalid_action"

        results.append({"action": action, "result": result})

        if result != "valid":
            all_valid = False

    summary = "VALID SEQUENCE" if all_valid else "INVALID SEQUENCE"

    return jsonify({"validation": results, "summary": summary})

if __name__ == "__main__":
    app.run()
