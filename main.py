from flask import Flask, request, Response
import yfinance as yf

app = Flask(__name__)

valid_periods = ['1d', '5d', '1mo',
                 '3mo', '6mo', '1y',
                 '2y', '5y', '10y',
                 'ytd', "max"]

valid_intervals = ['1m', '2m', '5m',
                   '15m', '30m', '60m',
                   '90m', '1h', '1d',
                   '5d', '1wk', '1mo', '3mo']


@app.route('/history', methods=['GET'])
def history():
    symbols = request.args.get('symbols')
    if symbols is None:
        return 'The required field symbols is not specified', 400

    period = request.args.get('period')
    interval = request.args.get('interval')

    if not 1 <= len(symbols.split(',')) <= 1000:
        return 'Symbols list length does not lie in the range from 1 to 1000', 400
    if period not in valid_periods:
        return f'Period {period} is not supported. Valid period: {valid_periods}', 400
    if interval not in valid_intervals:
        return f'Interval {interval} is not supported. Valid interval: {valid_intervals}', 400
    print(symbols, period, interval)

    response = {}
    for tick in symbols.split(','):
        try:
            quote = yf.Ticker(tick)
            info = quote.history(period=period, interval=interval).reset_index()
            info['Date'] = info['Date'].astype(str)

            holders = quote.institutional_holders

            response[tick] = {"info": info.T.to_dict(), "holders": holders.T.to_dict()}

        except:
            response[tick] = {"info": "no_history", "holders": "no_holders"}
    return response


@app.route('/options', methods=['GET'])
def options():
    symbol = request.args.get('symbol', default="AAPL")

    quote = yf.Ticker(symbol)
    info = quote.options
    check = bool(len(info))
    return {
        "result": check
    }


if __name__ == "__main__":
    app.run(debug=True)
