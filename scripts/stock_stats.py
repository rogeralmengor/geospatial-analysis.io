import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash import Dash, html, dcc

# --- Parameters ---
ticker_symbol = "AAPL"
years_back = 5  # for dividend screening
payout_ratio_threshold_low = 0.33
payout_ratio_threshold_high = 0.75

# --- Get dividend data ---
ticker = yf.Ticker(ticker_symbol)
dividends = ticker.dividends
dividends.index = dividends.index.tz_localize(None)
dividends = dividends[dividends.index >= (pd.Timestamp.today() - pd.DateOffset(years=years_back))]
div_per_year = dividends.groupby(dividends.index.year).sum()

# --- Get price data for 5 years ago ---
price_hist = ticker.history(period="7y")  # get extra data just in case
price_hist.index = price_hist.index.tz_localize(None)

price_5_years_ago_date = pd.Timestamp.today() - pd.DateOffset(years=years_back)
price_5_years_ago = price_hist.loc[price_hist.index >= price_5_years_ago_date]['Close'].iloc[0] if not price_hist.loc[price_hist.index >= price_5_years_ago_date].empty else None

# --- Criterion 1: cumulative dividend yield > 1% p.a. ---
if price_5_years_ago and len(dividends) > 0:
    cum_dividend = dividends.sum()
    cum_yield = (cum_dividend / price_5_years_ago) / years_back
else:
    cum_yield = 0

crit1 = cum_yield > 0.01

# --- Criterion 2: no dividend suspension (dividends every year for last 5 years) ---
years_present = set(div_per_year.index)
expected_years = set(range(pd.Timestamp.today().year - years_back + 1, pd.Timestamp.today().year + 1))
crit2 = expected_years.issubset(years_present)

# --- Criterion 3 & 4 & 5: dividend cuts / increases ---
div_years = div_per_year.sort_index()
# Calculate year-over-year dividend change
div_diff = div_years.diff()

# Criterion 3: no dividend cuts (no negative change)
crit3 = not any(div_diff.dropna() < 0)

# Criterion 4: at least two dividend increases
num_increases = sum(div_diff.dropna() > 0)
crit4 = num_increases >= 2

# Criterion 5: dividend increased last year (compare last 2 years)
if len(div_years) >= 2:
    crit5 = div_years.iloc[-1] > div_years.iloc[-2]
else:
    crit5 = False

# --- Criterion 6 & 7: smoothed payout ratio 3 years between 33% and 75% ---
info = ticker.info
payout_ratio = info.get("payoutRatio", None)
if payout_ratio is None:
    payout_ratio = 0.0

crit6 = payout_ratio < payout_ratio_threshold_high
crit7 = payout_ratio > payout_ratio_threshold_low

# --- Dividend Bar Chart (last 5 years) ---
div_fig = go.Figure([go.Bar(
    x=div_per_year.index.astype(str),
    y=div_per_year.values.flatten(),
    marker_color='#00C49F'
)])
div_fig.update_layout(
    title=f'{ticker_symbol} Annual Dividends (Last {years_back} Years)',
    xaxis_title='Year',
    yaxis_title='Total Dividends (USD)',
    template='plotly_dark'
)

# --- Payout Ratio Pie Chart ---
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

# --- Dividend Growth (last 5 years) ---
if len(div_per_year) >= 2:
    first_year = div_per_year.iloc[0]
    last_year = div_per_year.iloc[-1]
    growth_pct = ((last_year - first_year) / first_year) * 100
    growth_text = f"💰 {growth_pct:.1f}% dividend increase over the last {years_back} years"
else:
    growth_text = "Not enough data to calculate dividend growth"

# --- Create criteria table ---
criteria = [
    ("Cumulative dividend yield past 5 years > 1% p.a.", crit1),
    ("No dividend suspension in past 5 years", crit2),
    ("No dividend cuts in past 5 years", crit3),
    ("At least two dividend increases in past 5 years", crit4),
    ("Dividend increased in most recent year", crit5),
    ("Smoothed payout ratio last 3 years < 75%", crit6),
    ("Smoothed payout ratio last 3 years > 33%", crit7),
]

def generate_table(data):
    rows = []
    for desc, passed in data:
        check = "✔️" if passed else "❌"
        color = "#4CAF50" if passed else "#FF6B6B"
        rows.append(html.Tr([
            html.Td(desc, style={'padding': '8px'}),
            html.Td(check, style={'color': color, 'fontWeight': 'bold', 'textAlign': 'center', 'fontSize': '20px'})
        ]))
    return html.Table(
        # Header
        [html.Tr([html.Th("Screening Criteria", style={'textAlign': 'left', 'padding': '8px'}),
                  html.Th("Result", style={'textAlign': 'center', 'padding': '8px'})])] +
        rows,
        style={
            'width': '60%',
            'margin': '30px auto',
            'borderCollapse': 'collapse',
            'fontFamily': '"Segoe UI", "Roboto", sans-serif',
            'color': 'white',
            'backgroundColor': '#222222',
            'borderRadius': '8px',
            'boxShadow': '0 0 10px rgba(0,0,0,0.3)'
        }
    )

# --- Dash App ---
app = Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#111111',
        'color': 'white',
        'fontFamily': '"Segoe UI", "Roboto", sans-serif',
        'padding': '20px',
        'minHeight': '100vh',
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
        ]),
        generate_table(criteria)
    ]
)

if __name__ == '__main__':
    app.run(debug=True)
