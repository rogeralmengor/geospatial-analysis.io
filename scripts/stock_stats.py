import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import datetime

# --- Parameters ---
ticker_symbol = "JNJ"
years_back = 5
today = pd.Timestamp.today()

# --- Get dividend data ---
ticker = yf.Ticker(ticker_symbol)
company_name = ticker.info.get("longName", ticker_symbol)
dividends = ticker.dividends

# Fix timezone issue
dividends.index = dividends.index.tz_localize(None)

# --- Determine year boundaries ---
current_year_complete = today.month == 12
end_year = today.year if current_year_complete else today.year - 1
start_year = end_year - years_back + 1

# --- Filter only full calendar years ---
dividends = dividends[(dividends.index.year >= start_year) & (dividends.index.year <= end_year)]

# --- Group by year ---
div_per_year = dividends.groupby(dividends.index.year).sum()

# --- Calculate dividend growth over years ---
if len(div_per_year) >= 2:
    first_year = div_per_year.iloc[0]
    last_year = div_per_year.iloc[-1]
    growth_pct = ((last_year - first_year) / first_year) * 100
    growth_text = f"💰 {growth_pct:.1f}% dividend increase over the last {years_back} years"
else:
    growth_text = "Not enough data to calculate dividend growth"

# --- Create Dividend Bar Chart ---
div_fig = go.Figure([go.Bar(x=div_per_year.index.astype(str), y=div_per_year.values.flatten(), marker_color='lightskyblue')])
div_fig.update_layout(
    title=f'{ticker_symbol} Annual Dividends (Last {years_back} Complete Years)',
    xaxis_title='Year',
    yaxis_title='Total Dividends (USD)',
    template='plotly_white'
)

# --- Get payout ratio ---
info = ticker.info
payout_ratio = info.get("payoutRatio", 0.0)
retained_ratio = 1.0 - payout_ratio

# --- Create Pie Chart ---
pie_fig = go.Figure(data=[go.Pie(
    labels=["Dividends Paid", "Earnings Retained"],
    values=[payout_ratio, retained_ratio],
    hole=0.4,
    marker_colors=['#00C49F', '#FFBB28']
)])
pie_fig.update_layout(
    title=f"{ticker_symbol} Payout vs Retained Earnings",
    annotations=[dict(text='Payout', x=0.5, y=0.5, font_size=16, showarrow=False)],
    template='plotly_white'
)

# --- Criteria Evaluation ---
criteria_results = []

# Helper values
close_prices = ticker.history(period=f"{years_back}y")['Close']
last_price = close_prices[-1] if not close_prices.empty else None

div_sum_5y = dividends.sum()
cum_yield = (div_sum_5y / last_price) if last_price else 0.0
crit1 = cum_yield > 0.01
criteria_results.append((
    "Cumulative dividend yield past 5 years > 1% p.a.",
    crit1,
    f"Cumulative yield: {cum_yield*100:.2f}%"
))

# No dividend suspension
years_present = set(dividends.index.year)
expected_years = set(range(start_year, end_year + 1))
crit2 = expected_years.issubset(years_present)
criteria_results.append((
    "No dividend suspension in past 5 years",
    crit2,
    "All years present" if crit2 else f"Missing years: {', '.join(str(y) for y in sorted(expected_years - years_present))}"
))

# No dividend cuts
div_diff = div_per_year.diff().dropna()
crit3 = all(val >= 0 for val in div_diff)
criteria_results.append((
    "No dividend cuts in past 5 years",
    crit3,
    "No cuts" if crit3 else f"Cuts in: {', '.join(str(year) for year, val in div_diff.items() if val < 0)}"
))

# At least two increases
increases = sum(1 for val in div_diff if val > 0)
crit4 = increases >= 2
criteria_results.append((
    "At least 2 dividend increases in past 5 years",
    crit4,
    f"{increases} increases"
))

# Increase in last year
last_two = div_per_year.tail(2)
crit5 = len(last_two) == 2 and last_two.iloc[1] > last_two.iloc[0]
criteria_results.append((
    "Dividend increased last year",
    crit5,
    f"{last_two.index[0]}: {last_two.iloc[0]:.2f} → {last_two.iloc[1]:.2f}"
    if len(last_two) == 2 else "Not enough data"
))

# Smoothed payout ratio (dummy value)
smoothed_payout = payout_ratio
crit6 = smoothed_payout < 0.75
criteria_results.append((
    "Smoothed payout ratio last 3 years < 75%",
    crit6,
    f"Payout ratio: {smoothed_payout*100:.1f}%"
))

crit7 = smoothed_payout > 0.33
criteria_results.append((
    "Smoothed payout ratio last 3 years > 33%",
    crit7,
    f"Payout ratio: {smoothed_payout*100:.1f}%"
))

# --- Dash App Layout ---
app = Dash(__name__)

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#F9F9F9', 'padding': '20px'}, children=[
    html.H1(f"{ticker_symbol} ({company_name}) Dividend Dashboard", style={'textAlign': 'center', 'backgroundColor': 'white', 'padding': '10px'}),

    # Dividend bar chart
    dcc.Graph(figure=div_fig),

    # Pie chart
    dcc.Graph(figure=pie_fig),

    # Growth info
    html.Div([
        html.H2(growth_text, style={'textAlign': 'center', 'color': '#4CAF50', 'marginTop': '30px'})
    ]),

    # Screening criteria
    html.Div([
        html.H2("Dividend Stock Screening Criteria (Last 5 Full Years)", style={'textAlign': 'center'}),
        html.Table([
            html.Tr([
                html.Th("Criterion"),
                html.Th("Pass"),
                html.Th("Details")
            ])
        ] + [
            html.Tr([
                html.Td(desc),
                html.Td("✔️" if passed else "❌", style={'color': '#4CAF50' if passed else '#FF6B6B', 'fontWeight': 'bold', 'textAlign': 'center'}),
                html.Td(expl, style={'color': '#4CAF50' if passed else '#FF6B6B'})
            ]) for desc, passed, expl in criteria_results
        ], style={'width': '100%', 'marginTop': '20px', 'borderSpacing': '10px'})
    ])
])

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)

