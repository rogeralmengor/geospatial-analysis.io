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

# Fix timezone issue
dividends.index = dividends.index.tz_localize(None)

# Filter last 10 years
dividends = dividends[dividends.index >= (pd.Timestamp.today() - pd.DateOffset(years=years_back))]

# Group by year
div_per_year = dividends.groupby(dividends.index.year).sum()

# --- Create Dividend Bar Chart ---
div_fig = go.Figure([go.Bar(x=div_per_year.index.astype(str), y=div_per_year.values.flatten())])
div_fig.update_layout(
    title=f'{ticker_symbol} Annual Dividends (Last {years_back} Years)',
    xaxis_title='Year',
    yaxis_title='Total Dividends (USD)',
    template='plotly_dark'
)

# --- Get payout ratio ---
info = ticker.info
payout_ratio = info.get("payoutRatio", None)

# Default if missing
if payout_ratio is None:
    payout_ratio = 0.0

retained_ratio = 1.0 - payout_ratio

# --- Create Pie Chart ---
pie_fig = go.Figure(data=[go.Pie(
    labels=["Dividends Paid", "Earnings Retained"],
    values=[payout_ratio, retained_ratio],
    hole=0.4
)])
pie_fig.update_layout(
    title=f"{ticker_symbol} Payout vs Retained Earnings",
    annotations=[dict(text='Payout', x=0.5, y=0.5, font_size=16, showarrow=False)],
    template='plotly_dark'
)

# --- Dash App Layout ---
app = Dash(__name__)

app.layout = html.Div([
    html.H1(f"{ticker_symbol} Dividend Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(figure=div_fig),
    dcc.Graph(figure=pie_fig)
])

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
