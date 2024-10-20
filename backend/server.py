from flask import Flask
from flask_cors import CORS

from simulation import open_bill

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/start_sim', methods=['GET'])
def start_sim():
    """
    Starts the simulation. Processes a bill into a list of clauses and returns them.
    """

    clauses = {"clauses": open_bill()}
    return clauses

@app.route('/initial-agreement-level')
def initial_agreement_level():
    """
    Input: takes in a clause in plaintext
    Output: ids of the min and max agreement senators
    """
    pass

@app.route('/debate')
def debate():
    """
    Input: senator id, current clause
    Output: updated clause 
    """
    pass

@app.route('/vote')
def vote():
    """
    Input: updated clause
    Output: whether or not majority have agreed 
    """

# Run the application
if __name__ == '__main__':
    app.run(debug=True, port=8080)
