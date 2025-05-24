import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, html, dcc

# --- Parameters ---
ticker_symbol = "AAPL"
years_back = 10

# --- Get dividend data ---
ticker = yf.Ticker(ticker_symbol)
dividends = ticker.dividends
dividends.index = dividends.index.tz_localize(None)
dividends = dividends[dividends.index >= (pd.Timestamp.today() - pd.DateOffset(years=years_back))]
div_per_year = dividends.groupby(dividends.index.year).sum()

# --- Calculate dividend growth ---
if len(div_per_year) >= 2:
    first_year = div_per_year.iloc[0]
    last_year = div_per_year.iloc[-1]
    growth_pct = ((last_year - first_year) / first_year) * 100
    growth_text = f"💰 {growth_pct:.1f}% dividend increase over the last {years_back} years"
else:
    growth_text = "Not enough data to calculate dividend growth"

# --- Dividend Bar Chart ---
div_fig = go.Figure([go.Bar(x=div_per_year.index.astype(str), y=div_per_year.values.flatten(),  marker_color='#00C49F')])
div_fig.update_layout(
    title=f'{ticker_symbol} Annual Dividends (Last {years_back} Years)',
    xaxis_title='Year',
    yaxis_title='Total Dividends (USD)',
    template='plotly_dark'
)

# --- Payout Ratio Pie Chart ---
info = ticker.info
payout_ratio = info.get("payoutRatio", 0.0)
retained_ratio = 1.0 - payout_ratio

pie_fig = go.Figure(data=[go.Pie(
    labels=["Dividends Paid", "Earnings Retained"],
    values=[payout_ratio, retained_ratio],
    hole=0.4,
    marker=dict(colors=['#FF6B6B', '#4ECDC4'])
)])
pie_fig.update_layout(
    title=f"{ticker_symbol} Payout vs Retained Earnings",
    annotations=[dict(text='Payout', x=0.5, y=0.5, font_size=16, showarrow=False)],
    template='plotly_dark'
)

# --- Dash App ---
app = Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#111111',
        'color': 'white',
        'fontFamily': '"Segoe UI", "Roboto", sans-serif',
        'padding': '20px'
    },
    children=[
        html.H1(f"{ticker_symbol} Dividend Dashboard", style={'textAlign': 'center'}),
        dcc.Graph(figure=div_fig),
        dcc.Graph(figure=pie_fig),
        html.Div([
            html.H2(growth_text, style={
                'textAlign': 'center',
                'color': '#4CAF50',
                'marginTop': '30px'
            })
        ])
    ]
)

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
