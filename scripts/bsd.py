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

