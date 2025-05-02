from flask import Flask, request, jsonify, render_template
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


@app.get("/stocks")
def get_stocks():
    ticker= request.args.get("ticker")
    data=yf.Ticker(ticker)
    data = data.history(period="1d")
    if data.empty:
        return {"message": f"No data found for ticker '{ticker}'"}, 404
    data.reset_index(inplace=True)
    data["Date"] = data["Date"].dt.strftime('%Y-%m-%d')
    return jsonify(data.to_dict(orient="records"))




@app.route("/chart")
def index():
    ticker = request.args.get("ticker")
    data = yf.Ticker(ticker).history(period="1y")
    data.reset_index(inplace=True)
    chart_data = {
        "labels": data["Date"].dt.strftime('%Y-%m-%d').tolist(),
        "open": data["Open"].tolist(),
        "close": data["Close"].tolist()
    }
    return chart_data


@app.route("/")
def home():
    return render_template("chart.html")



if __name__=="__main__":
    app.run(debug=True)
