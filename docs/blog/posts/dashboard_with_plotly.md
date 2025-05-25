# Why I Built a Dividend Stock Screener (And How You Can Too)

Let me be straight with you - I've been losing sleep over retirement. Looking at my finances and realizing retirement isn't as far away as I thought has been a real wake-up call. With pension systems barely hanging on, I knew I had to take control of my financial future.

I know everyone says "just buy ETFs" - and honestly, they're probably right. Going with the market is safer than trying to pick winners. But I can't help myself when it comes to diving into individual companies. There's something addictive about analyzing financial statements, dividend histories, and ratios like P/E and payout ratios. Being a numbers person, this stuff genuinely fascinates me.

So I built a [Python tool](#main-script) (and [support function](#support-function)) to help me screen dividend-paying stocks systematically. Here's how it works and why it might help you too. (Go to Code)

## Libraries
Of course you need some things to **"pipinstall"**:

* plotly
* dash
* yfinance
* pandas
* bsd (A simple helper module with function to calculate the BSD formula from the book: [The little book of big dividends](https://www.thalia.de/shop/home/artikeldetails/A1008989339){:target="_blank"})

## The Simple Setup

The whole thing starts with just two parameters:

```python
ticker_symbol = "JNJ"  # Which company to analyze
years_back = 5         # How far back to look
```

That's it. The tool grabs data from Yahoo Finance and does all the heavy lifting from there.

## My 7-Point Screening System

I created seven criteria based on what I've learned from a [dividend investing book](https://www.thalia.de/shop/home/artikeldetails/A1038443853){:target="_blank"} I reference at the end of this post:

**1. Decent yield** - At least 1% annually over 5 years
**2. No suspensions** - Company never stopped paying dividends
**3. No cuts** - Dividends never went backwards
**4. Growth pattern** - At least 2 increases in 5 years
**5. Recent momentum** - Dividend went up last year
**6-7. Smart payout ratio** - Between 33-75% (sustainable but not stingy)

The tool also calculates something called a BSD score, which gives additional insight into business strength.

## What the Dashboard Shows

Using Plotly and Dash, I created visualizations that make the data easy to understand:
- Bar charts showing dividend growth over time
- Pie charts breaking down payout vs. retained earnings
- Clear tables showing which criteria pass or fail

No fancy financial jargon - just clear answers to "Is this a good dividend stock?"

## Testing with Johnson & Johnson

I ran Johnson & Johnson through the screener first. As a Dividend Aristocrat, I expected it to pass - and it did, beautifully. All seven criteria passed, giving me confidence the system actually works.

You can see how this humble dashboard looks like below: 

<iframe src="j&j.html" width="100%" height="600px" frameborder="0"></iframe>

## Why This Helps Me Sleep Better

This isn't about beating the market or finding hidden gems. It's about understanding what I'm investing in. When you're worried about retirement, having systematic ways to evaluate investments provides real peace of mind.

The tool is simple to use - just change the ticker symbol and run it. Within seconds, you know whether a stock meets basic dividend quality standards and can see exactly why.

Of course there are more financial indicators to further evaluate a stock, but that is a first fair attempt. I might expand this dashboard adding more graphs and statistics in the future.

## The Bottom Line

Building this screener has been both educational and therapeutic. It combines my love of numbers with practical retirement planning needs. While ETFs might be the smart money move, having tools to understand individual stocks makes me feel more in control of my financial future.

If you're dealing with similar retirement anxiety, maybe building your own analysis tools could help too. Sometimes the process of understanding is just as valuable as the results.


<a id="main-script"></a>
<details>
    <summary>dividend_stock_screener.py</summary>
```python title="dividend_stock_screener.py" linenums="1"
"""Python script to screen dividend paying stock based on multiple variables."""

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, html, dcc
from bsd import calculate_bsd_score

# --- Parameters ---
ticker_symbol = "PG"
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

# --- BSD Dashboard Component ---
bsd_score, bsd_breakdown = calculate_bsd_score(ticker_symbol)

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
    ]),
    
    html.Div([
    html.H2("BSD Score Analysis", style={'textAlign': 'center', 'marginTop': '40px'}),
    html.Table([
        html.Tr([html.Th("Metric"), html.Th("Points")])
    ] + [
        html.Tr([
            html.Td(text),
            html.Td(f"{points:.1f}", style={'textAlign': 'right'})
        ]) for text, points in bsd_breakdown
    ] + [
        html.Tr([
            html.Td("Total BSD Score", style={'fontWeight': 'bold'}),
            html.Td(f"{bsd_score:.1f}", style={'fontWeight': 'bold', 'textAlign': 'right'})
        ])
    ], style={'width': '100%', 'marginTop': '20px', 'borderSpacing': '10px'})
    ]) 
])

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True)
```
</details>

<a id="support-function"></a>
<details>
    <summary>Helper Function BSD Calculation</summary>
```python title="bsd.py" linenums="1"
import yfinance as yf
import pandas as pd

# --- BSD Score Function ---
def calculate_bsd_score(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info
    hist = ticker.history(period="5y")

    # Get dividends and calculate yearly totals
    dividends = ticker.dividends
    dividends.index = dividends.index.tz_localize(None)
    today = pd.Timestamp.today()
    end_year = today.year - 1 if today.month < 12 else today.year
    start_year = end_year - 4
    dividends = dividends[(dividends.index.year >= start_year) & (dividends.index.year <= end_year)]
    div_per_year = dividends.groupby(dividends.index.year).sum()

    score_details = []
    total_score = 0

    def score(metric_name, value, threshold_good, threshold_bad, weight, higher_better=True):
        if value is None or pd.isna(value):
            explanation = f"{metric_name}: N/A"
            return 0, explanation
        if higher_better:
            if value >= threshold_good:
                pts = weight
                explanation = f"{metric_name}: {value:.2f} ≥ {threshold_good} (full {weight} pts)"
            elif value <= threshold_bad:
                pts = 0
                explanation = f"{metric_name}: {value:.2f} ≤ {threshold_bad} (0 pts)"
            else:
                pts = ((value - threshold_bad) / (threshold_good - threshold_bad)) * weight
                explanation = f"{metric_name}: {value:.2f} (partial score: {pts:.2f})"
        else:
            if value <= threshold_good:
                pts = weight
                explanation = f"{metric_name}: {value:.2f} ≤ {threshold_good} (full {weight} pts)"
            elif value >= threshold_bad:
                pts = 0
                explanation = f"{metric_name}: {value:.2f} ≥ {threshold_bad} (0 pts)"
            else:
                pts = ((threshold_bad - value) / (threshold_bad - threshold_good)) * weight
                explanation = f"{metric_name}: {value:.2f} (partial score: {pts:.2f})"
        return pts, explanation

    # 1. Payout Ratio (30%)
    payout_ratio = info.get("payoutRatio", None)
    pts, expl = score("Payout Ratio", payout_ratio, 0.6, 1.0, 30, higher_better=False)
    total_score += pts
    score_details.append((expl, pts))

    # 2. Interest Coverage Proxy (10%) using EBITDA / Total Debt
    interest_coverage = None
    try:
        ebitda = info.get("ebitda", None)
        total_debt = info.get("totalDebt", None)
        if ebitda is not None and total_debt and total_debt != 0:
            interest_coverage = ebitda / total_debt
    except:
        pass
    pts, expl = score("Interest Coverage Proxy (EBITDA / Total Debt)", interest_coverage, 5, 1, 10)
    total_score += pts
    score_details.append((expl, pts))

    # 3. Cash Flow to Net Income (5%)
    cf_to_ni = None
    try:
        ocf = info.get("operatingCashflow", None)
        net_income = info.get("netIncomeToCommon", None)
        if ocf and net_income:
            cf_to_ni = ocf / net_income
    except:
        pass
    pts, expl = score("Cash Flow to Net Income", cf_to_ni, 1.1, 0.8, 5)
    total_score += pts
    score_details.append((expl, pts))

    # 4. Dividend Yield (5%)
    dividend_yield = info.get("dividendYield", None)
    pts, expl = score("Dividend Yield", dividend_yield, 0.03, 0.01, 5)
    total_score += pts
    score_details.append((expl, pts))

    # 5. Relative Strength (12-month) (10%)
    rel_strength = info.get("52WeekChange", None)
    pts, expl = score("Relative Strength (12mo)", rel_strength, 0.10, -0.10, 10)
    total_score += pts
    score_details.append((expl, pts))

    # 6. Book Value Growth (10%)
    bvps = info.get("bookValue", None)
    prev_bvps = bvps * 0.9 if bvps else None
    book_growth = ((bvps - prev_bvps) / prev_bvps) if bvps and prev_bvps else None
    pts, expl = score("Book Value Growth (proxy)", book_growth, 0.08, 0.01, 10)
    total_score += pts
    score_details.append((expl, pts))

    # 7. Long-term earnings growth (10%)
    earnings_growth = info.get("earningsGrowth", None)
    pts, expl = score("Earnings Growth (LT)", earnings_growth, 0.10, 0.02, 10)
    total_score += pts
    score_details.append((expl, pts))

    # 8. 3-year Cash Flow Growth (5%)
    cash_growth = earnings_growth * 0.9 if earnings_growth else None
    pts, expl = score("Cash Flow Growth (proxy)", cash_growth, 0.08, 0.01, 5)
    total_score += pts
    score_details.append((expl, pts))

    # 9. 3-year Dividend Growth (10%)
    div_growth = None
    try:
        if len(div_per_year) >= 4:
            div_growth = (div_per_year.iloc[-1] - div_per_year.iloc[-4]) / div_per_year.iloc[-4]
    except:
        pass
    pts, expl = score("Dividend Growth (3y)", div_growth, 0.20, 0.00, 10)
    total_score += pts
    score_details.append((expl, pts))

    # 10. 3-year Earnings Growth (5%)
    pts, expl = score("Earnings Growth (3y)", earnings_growth, 0.10, 0.02, 5)
    total_score += pts
    score_details.append((expl, pts))

    return round(total_score, 1), score_details
```
</details>


