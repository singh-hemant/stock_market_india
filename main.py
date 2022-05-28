from dash import Dash, html, dcc, Input, Output, dash_table
import yfinance as yf
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_extensions as de


# for table
no_of_companies = 50
df = pd.read_excel("companies_by_mc.xlsx", header=0, nrows=no_of_companies)
table_stocks = pd.DataFrame({'Name':[], 'MarketCap':[], 'Open':[], 'Gain/Loss':[], 'G/L %':[]})
for i in range(len(df.index)):
    h = yf.Ticker(df['Ticker'][i]).history(period='2d', interval='1d')
    gl = round(h['Close'][-1] - h['Close'][-2], 3)
    glp = round((gl/h['Close'][-2])*100, 3)
    temp = pd.DataFrame({'Name':[df['Company Name'][i]],
                         'MarketCap':[round(df['MarketCap(in_Lakhs)'][i], 3)],
                         'Open':[round(h['Close'][-1], 3)], 'Gain/Loss':[gl], 'G/L %':[glp]})
    table_stocks = pd.concat([table_stocks, temp], ignore_index=True)
    

# Lottie animation urls
url0 = "https://assets1.lottiefiles.com/packages/lf20_wvntgftp.json"
url1 = "https://assets7.lottiefiles.com/private_files/lf30_khwfxgwr.json"
gold_url = "https://assets1.lottiefiles.com/packages/lf20_o8VNah.json"
btc_url = "https://assets8.lottiefiles.com/packages/lf20_oNHjED.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))


def get_stats(code):
    t = yf.Ticker(code)
    hist_t = t.history(period='1d', interval='1m')
    t_curr = round(hist_t.iloc[-1]['Open'], 3)
    gl_t = round(t_curr - hist_t.iloc[-2]['Open'], 2)
    gl_percent_t = round(((t_curr - hist_t.iloc[-2]['Open'])/hist_t.iloc[-2]['Open'])*100, 2)
    return t_curr, gl_t, gl_percent_t


def colors(n):
    if n==0:
        return '#0096FF' #blue
    elif n > 0:
        return '#90ee90' # green
    else:
        return '#EE4B2B' # red
              


# NIfty data
nifty_curr, gl_nifty, gl_percent_nifty = get_stats('^NSEI')

# SENSEX data
sensex_curr, gl_sensex, gl_percent_sensex = get_stats('^BSESN')

# GOLD data
gold_curr, gl_gold, gl_percent_gold = get_stats('GC=F')

# RUPEE data
rupee_curr, gl_rupee, gl_percent_rupee = get_stats('INR=X')

# BITCOIN data
bitcoin_curr, gl_bitcoin, gl_percent_bitcoin = get_stats('BTC-USD')


app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO], meta_tags=[{
                                                                            'name':'viewport',
                                                                            'content':'width-device-width,initial-scale=1.0,maximum-scale=1.2,minimum-scale=0.5,'
                                                                            }])
server = app.server

app.layout = dbc.Container([
        html.Br(),
        dcc.Interval(
                    id='interval-component',
                    interval=1*3000, # in milliseconds
                    n_intervals=0
                ),

        dbc.Row([
            html.H1("STOCK EXCHANGE INDIA")
            ], style={'text-align':'center'}),
        html.Hr(),
         
        dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardHeader("NIFTY"),
                    dbc.Row([
                    dbc.Col(
                        dbc.CardBody([
                            html.H4(str(nifty_curr), id='nifty'),
                            html.P(f"{str(gl_nifty)} ({str(gl_percent_nifty)} %)", id='nifty_percent'),
                            ],id='body_nifty'),
                        class_name="col-md-7"),
                    dbc.Col(de.Lottie(options=options, width="100%", height="100%", url=url0),class_name="col-md-5") ])
                    ]), md=3),
                                 
                dbc.Col(dbc.Card([
                    dbc.CardHeader("SENSEX"),
                    dbc.Row([
                    dbc.Col(
                        dbc.CardBody([
                            html.H4(str(sensex_curr), id='sensex'),
                            html.P(f"{str(gl_sensex)} ({str(gl_percent_sensex)}%)", id='sensex_percent')
                            ],id='body_sensex'),
                        class_name="col-md-7"),
                    dbc.Col(de.Lottie(options=options, width="80%", height="100%", url=url1),class_name="col-md-5") ])
                        ]), md=3),
                dbc.Col(dbc.Card([
                    dbc.CardHeader("GOLD"),
                    dbc.Row([
                    dbc.Col(
                        dbc.CardBody([
                            html.H4(str(gold_curr), id='gold'),
                            html.P(f"{str(gl_gold)} ({str(gl_percent_gold)} %)", id='gold_percent')
                            ],id='body_gold'),
                        class_name="col-md-7"),
                    dbc.Col(de.Lottie(options=options, width="100%", height="100%", url=gold_url),class_name="col-md-5") ])
                    ]), md=3),
                dbc.Col(dbc.Card([
                    dbc.CardHeader("BITCOIN"),
                    dbc.Row([
                    dbc.Col(
                        dbc.CardBody([
                            html.H4(str(bitcoin_curr), id='bitcoin'),
                            html.P(f"{str(gl_bitcoin)} ({str(gl_percent_bitcoin)} %)", id='bitcoin_percent')
                            ],id='body_btc'),
                        class_name="col-md-7"),
                    dbc.Col(de.Lottie(options=options, width="100%", height="100%", url=btc_url),class_name="col-md-5") ])
                    ]), md=3),
                
            ]),
        html.Hr(),
        
        dbc.Row(
            [
                dbc.Col(html.Div([
                    dcc.Graph(id='main'),

                    ])),
                
                dbc.Col([
                    html.Br(),
                    html.H4("Plot type"),
                    dcc.Dropdown(   
                        options=[
                            {'label': 'CandlePlot', 'value': 'candle'},
                            {'label': 'OHLC', 'value': 'ohlc'},
                            {'label': 'LINE', 'value': 'line'},
                        ],
                        value='candle',
                        id = "plot_type",
                        style={'color':'green'}
                    ),
                    html.Hr(),
                    
                    html.H4("Stock Name"),
                    dcc.Dropdown(   
                        options=[
                            {'label': 'Nifty', 'value': '^NSEI'},
                            {'label': 'SENSEX', 'value': '^BSESN'},
                            {'label': 'GOLD', 'value': 'GC=F'},
                            {'label': 'BITCOIN', 'value': 'BTC-USD'},
                        ],
                        value='^NSEI',
                        id = "stock_type",
                        style={'color':'green'}
                    ),
                    html.Hr(),

                    html.H4("Time Period"),
                    dcc.Dropdown(    
                        options=[
                            {'label': 'One Day', 'value': '1d'},
                            {'label': 'Five Days', 'value': '5d'},
                            {'label': 'One Month', 'value': '1mo'},
                            {'label': 'Three Months', 'value': '3mo'},
                            {'label': 'Six Months', 'value': '6mo'},
                            {'label': 'One Year', 'value': '1y'},
                            {'label': 'Two Years', 'value': '2y'},
                            {'label': 'Five Years', 'value': '5y'},
                            {'label': 'Ten Years', 'value': '10y'},
                            {'label': 'Yesterday', 'value': 'ytd'},
                            {'label': 'All Data', 'value': 'max'},
                        ],
                        value='6mo',
                        id = "period",
                        style={'color':'green'}
                    ),

                    html.Hr(),

                    html.H4("Interval"),
                    dcc.Dropdown(    
                        options=[
                            #{'label': 'One Minute', 'value': '1m'},
                           # {'label': 'Two Minutes', 'value': '2m'},
                            #{'label': 'Five minutes', 'value': '5m'},
                            #{'label': 'Fifteen minutes', 'value': '15m'},
                            #{'label': '30 minutes', 'value': '30m'},
                            {'label': '60 minutes', 'value': '60m'},
                            {'label': '90 minutes', 'value': '90m'},
                            {'label': 'One hour', 'value': '1h'},
                            {'label': 'One day', 'value': '1d'},
                            {'label': '5day', 'value': '5d'},
                            {'label': 'One week', 'value': '1wk'},
                            {'label': 'One Month', 'value': '1mo'},
                            {'label': 'Three Months', 'value': '3mo'},
                        ],
                        value='1d',
                        id = "interval",
                        style={'color':'green'}
                    )

                    ], md=2),
            ]
        ),
        html.Hr(),

        html.H4(f"Top {no_of_companies} Companies by Market Cap", style={"text-align":'center'}),
        html.Br(),
        dbc.Row(
            dash_table.DataTable(
                data = table_stocks.to_dict('records'),
                sort_action='native',
                columns = [
                        {'name':'Name', 'id':'Name', 'type':'text'},
                        {'name':'Market Cap', 'id':'MarketCap', 'type':'numeric'},
                        {'name':'Current Price', 'id':'Open', 'type':'numeric'},
                        {'name':'Gain/Loss', 'id':'Gain/Loss', 'type':'numeric'},
                        {'name':'Gain/Loss(%)', 'id':'G/L %', 'type':'numeric'},
                    ],
                    editable=False,
                    style_header={
                        'backgroundColor': 'rgb(210, 210, 210)',
                        'color': 'black',
                        'fontWeight': 'bold',
                        'textAlign':'center',
                        },
                    style_data_conditional=[
                        {
                            'background':'transparent',
                            'textAlign':'left',
                        },
                        {
                            'if': {
                                'filter_query': '{Gain/Loss} =0',
                                'column_id': 'Gain/Loss'
                            },
                            'backgroundColor':  '#0096FF', #blue
                            },
                        {
                            'if': {
                                'filter_query': '{Gain/Loss} > 0',
                                'column_id': 'Gain/Loss'
                            },
                            'backgroundColor': '#3D9970',
                            'color': 'white'
                            },
                        {
                            'if': {
                                'filter_query': '{Gain/Loss} < 0',
                                'column_id': 'Gain/Loss'
                            },
                            'backgroundColor': '#FF4136',
                            'color': 'white'
                            },

                        {
            
                            'if': {
                                'filter_query': '{G/L %} =0',
                                'column_id': 'G/L %'
                            },
                            'backgroundColor':  '#0096FF', #blue
                            },
                        {
                            'if': {
                                'filter_query': '{G/L %} > 0',
                                'column_id': 'G/L %'
                            },
                            'backgroundColor': '#3D9970',
                            'color': 'white'
                            },
                        {
                            'if': {
                                'filter_query': '{G/L %} < 0',
                                'column_id': 'G/L %'
                            },
                            'backgroundColor': '#FF4136',
                            'color': 'white'
                            },
                        ],

                )
        )
    
        
    ])


# Nifty live update collback func
@app.callback(
    Output('nifty', 'children'),
    Output('nifty_percent', 'children'),
    Output('nifty_percent', 'style'),
    Input('interval-component', 'n_intervals'))
def update_nifty(n):
    nifty_curr, gl_nifty, gl_percent_nifty = get_stats('^NSEI')
    color = colors(gl_nifty)
    return nifty_curr, f"{str(gl_nifty)} ({str(gl_percent_nifty)} %)", {'color':color}

# Sensex live update collback func
@app.callback(
    Output('sensex', 'children'),
    Output('sensex_percent', 'children'),
    Output('sensex_percent', 'style'),
    Input('interval-component', 'n_intervals'))
def update_sensex(n):
    sensex_curr, gl_sensex, gl_percent_sensex = get_stats('^BSESN')
    color = colors(gl_sensex)
    return sensex_curr, f"{str(gl_sensex)} ({str(gl_percent_sensex)} %)", {'color':color}

# Gold live update collback func
@app.callback(
    Output('gold', 'children'),
    Output('gold_percent', 'children'),
    Output('gold_percent', 'style'),
    Input('interval-component', 'n_intervals'))
def update_gold(n):
    gold_curr, gl_gold, gl_percent_gold = get_stats('GC=F')
    color = colors(gl_gold)
    return gold_curr, f"{str(gl_gold)} ({str(gl_percent_gold)} %)", {'color':color}

# Bitcoin live update collback func
@app.callback(
    Output('bitcoin', 'children'),
    Output('bitcoin_percent', 'children'),
    Output('bitcoin_percent', 'style'),
    Input('interval-component', 'n_intervals'))
def update_bitcoin(n):
    bitcoin_curr, gl_bitcoin, gl_percent_bitcoin = get_stats('BTC-USD')
    color = colors(gl_bitcoin)
    return bitcoin_curr, f"{str(gl_bitcoin)} ({str(gl_percent_bitcoin)} %)", {'color':color}



@app.callback(
    Output('main', 'figure'),
    Input('stock_type', 'value'),
    Input('period', 'value'),
    Input('interval', 'value'),
    Input('plot_type', 'value'))
def update_main(stock="^NSEI", period="6mo", interval='1d', plot_type='candle'):
    template='ggplot2'
    history = yf.Ticker(stock).history(period=period, interval=interval)
    if plot_type=='line':
        fig = go.Figure(data=[go.Line(x=history.index, y=history['Close'])])
        fig.update_yaxes(title=None, ticklabelposition='inside')
        fig.update_xaxes(title=None, ticklabelposition='inside')
        fig.update_layout(template=template,
        margin=dict(l=0, r=0, t=0, b=0),)
        return fig
    if plot_type=='ohlc':
        fig = go.Figure(data=[go.Ohlc(x=history.index, open=history['Open'], high=history['High'], low=history['Low'], close=history['Close'])])
        fig.update_yaxes(title=None, ticklabelposition='inside')
        fig.update_xaxes(title=None, ticklabelposition='inside')
        fig.update_layout(template=template,
        margin=dict(l=0, r=0, t=0, b=0),)
        return fig
    else:
        fig = go.Figure(data=[go.Candlestick(x=history.index, open=history['Open'], high=history['High'], low=history['Low'], close=history['Close'])])
        fig.update_yaxes(title=None, ticklabelposition='inside')
        fig.update_xaxes(title=None, ticklabelposition='inside')
        fig.update_layout(template=template,
        margin=dict(l=0, r=0, t=0, b=0),)
        return fig



if __name__ == "__main__":
    app.run_server(debug=True)
