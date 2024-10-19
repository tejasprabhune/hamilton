from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

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
    app.run(debug=True)
