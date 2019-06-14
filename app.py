from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, show
from bokeh.palettes import Set1 as palette
from bokeh.embed import components

import requests
import itertools

def _convert_date(s, fmt='%Y-%m-%d'):
    output = pd.to_datetime(s, format=fmt)
    return output

def _url(stock, columns):
    if type(columns) is not list:
        columns = [columns]
    columns.append('date')
    api_key = 'api_key=T1uisS-t1xu7ASeQHMzx'
    url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.csv?'
    keys = 'qopts.columns=' + ','.join(columns)
    ticker = 'ticker=%s' %(stock.upper())

    output = url + keys + '&' + ticker + '&' + api_key

    return output

def query_date(stock, columns):
    url = _url(stock, columns)

    try:
        output = pd.read_csv(url)
    except:
        return 'File not found'
    output['date'] = output['date'].apply(_convert_date)
    output.set_index('date', inplace=True)

    return output

def plot_data(data, height=300, sizing_mode='scale_width', tools='pan,box_zoom,wheel_zoom,reset,crosshair,hover,save', **kwargs):
    end = pd.to_datetime('2018-1-1')
    beginning = end - pd.DateOffset(years=1)
    dates = {'gte': beginning, 'lte': end}

    x = data.index
    colors = itertools.cycle(palette[8])

    p = figure(tools=tools, title=stock.upper(), x_axis_label='Date', y_axis_label='Value', x_axis_type='datetime')
    for key, color in zip(data.columns, colors):
        p.line(x, data[key], color=color, legend=key)
    p.legend.location = 'bottom_left'
    script, div = components(p)

    return script, div

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(port=33507)
