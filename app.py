from flask import Flask, request
import levy

app = Flask(__name__)


@app.route('/getlevyparameter', methods=['POST'])
def get_levy_parameter():
    if request.method == 'POST':
        body = request.get_json()
        quotationdate = body['quotationdate']
    try:
        result=levy.get_levy_parameter(quotationdate)
        response = {
            "Result": result,
            "Error": None
        }
    except Exception as e:
        response = {
            "Result": None,
            "Error": str(e)
        }
    return response

@app.route('/quotelevy', methods=['POST'])
def quote_levy():
    if request.method == 'POST':
        body = request.get_json()
        modalpremium=body['modalpremium']
        currency=body['currency']
        quotationdate = body['quotationdate']
    try:
        result=levy.quote_levy(modalpremium,currency,quotationdate)
        response = {
            "Result": result,
            "Error": None
        }
    except Exception as e:
        response = {
            "Result": None,
            "Error": str(e)
        }
    return response

@app.route('/levyschedule', methods=['POST'])
def levy_schedule():
    if request.method == 'POST':
        body = request.get_json()
        modalpremium=body['modalpremium']
        paymentterm = body['paymentterm']
        mode = body['mode']
        currency=body['currency']
        startdate = body['startdate']
    try:
        result=levy.levy_schedule(modalpremium, paymentterm, mode, currency, startdate)
        response = {
            "Result": result,
            "Error": None
        }
    except Exception as e:
        response = {
            "Result": None,
            "Error": str(e)
        }
    return response

if __name__ == '__main__':
    app.run(debug=True, host='localhost')
