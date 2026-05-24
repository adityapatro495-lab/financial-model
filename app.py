from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)


# ---------------------------------------------------
# Utility
# ---------------------------------------------------

def round_value(value):
    return round(value, 2)


# ---------------------------------------------------
# Asset Forecast Engine
# ---------------------------------------------------

def forecast_asset(
    opening,
    monthly_investment,
    annual_return,
    years,
    asset_name
):

    data = []

    balance = float(opening)

    monthly_rate = annual_return / 12

    total_invested = opening

    for year in range(1, years + 1):

        opening_balance = balance

        yearly_investment = 0

        yearly_growth = 0

        for month in range(12):

            balance += monthly_investment

            yearly_investment += monthly_investment

            total_invested += monthly_investment

            growth = balance * monthly_rate

            balance += growth

            yearly_growth += growth

        data.append({

            "Year": year,
            "Asset": asset_name,
            "Opening": round_value(opening_balance),
            "Investment": round_value(yearly_investment),
            "Growth": round_value(yearly_growth),
            "Closing": round_value(balance),
            "Total Invested": round_value(total_invested)

        })

    return pd.DataFrame(data)


# ---------------------------------------------------
# FD Forecast
# ---------------------------------------------------

def forecast_fd(
    opening,
    monthly_deposit,
    annual_interest,
    years,
    asset_name
):

    data = []

    balance = float(opening)

    monthly_rate = annual_interest / 12

    total_invested = opening

    for year in range(1, years + 1):

        opening_balance = balance

        yearly_deposit = 0

        yearly_interest = 0

        for month in range(12):

            balance += monthly_deposit

            yearly_deposit += monthly_deposit

            total_invested += monthly_deposit

            interest = balance * monthly_rate

            balance += interest

            yearly_interest += interest

        data.append({

            "Year": year,
            "Asset": asset_name,
            "Opening": round_value(opening_balance),
            "Investment": round_value(yearly_deposit),
            "Interest": round_value(yearly_interest),
            "Closing": round_value(balance),
            "Total Invested": round_value(total_invested)

        })

    return pd.DataFrame(data)


# ---------------------------------------------------
# SWP Forecast
# ---------------------------------------------------

def swp_forecast(
    corpus,
    annual_return,
    annual_withdrawal,
    withdrawal_increase,
    max_years=100
):

    data = []

    balance = float(corpus)

    monthly_return = annual_return / 12

    current_withdrawal = annual_withdrawal

    year = 1

    while balance > 0 and year <= max_years:

        opening_balance = balance

        yearly_growth = 0

        yearly_withdrawal = 0

        monthly_withdrawal = current_withdrawal / 12

        for month in range(12):

            growth = balance * monthly_return

            balance += growth

            yearly_growth += growth

            balance -= monthly_withdrawal

            yearly_withdrawal += monthly_withdrawal

            if balance <= 0:

                balance = 0

                break

        data.append({

            "Year": year,
            "Opening Corpus": round_value(opening_balance),
            "Growth": round_value(yearly_growth),
            "Annual Withdrawal": round_value(yearly_withdrawal),
            "Monthly Withdrawal": round_value(monthly_withdrawal),
            "Closing Corpus": round_value(balance)

        })

        current_withdrawal *= (1 + withdrawal_increase)

        year += 1

    return pd.DataFrame(data)


# ---------------------------------------------------
# Routes
# ---------------------------------------------------

@app.route("/")
def index():

    return render_template("index.html")


@app.route("/run_forecast", methods=["POST"])
def run_forecast():

    try:

        data = request.json

        years = int(data["years"])

        # ---------------------------------------------------
        # Equity
        # ---------------------------------------------------

        equity_opening = float(data["equity_opening"])
        equity_monthly = float(data["equity_monthly"])
        equity_cagr = float(data["equity_cagr"]) / 100

        # ---------------------------------------------------
        # FD
        # ---------------------------------------------------

        fd_opening = float(data["fd_opening"])
        fd_monthly = float(data["fd_monthly"])
        fd_cagr = float(data["fd_cagr"]) / 100

        # ---------------------------------------------------
        # Bonds
        # ---------------------------------------------------

        bonds_opening = float(data["bonds_opening"])
        bonds_monthly = float(data["bonds_monthly"])
        bonds_cagr = float(data["bonds_cagr"]) / 100

        # ---------------------------------------------------
        # Gold
        # ---------------------------------------------------

        gold_opening = float(data["gold_opening"])
        gold_monthly = float(data["gold_monthly"])
        gold_cagr = float(data["gold_cagr"]) / 100

        # ---------------------------------------------------
        # SWP
        # ---------------------------------------------------

        corpus_reduction = float(data["tax_rate"]) / 100

        withdraw_amount = float(data["withdraw_amount"])

        withdraw_increase = float(data["withdraw_increase"]) / 100

        growth_rate = float(data["growth_rate"]) / 100

        # ---------------------------------------------------
        # Forecast Calculations
        # ---------------------------------------------------

        equity_df = forecast_asset(
            equity_opening,
            equity_monthly,
            equity_cagr,
            years,
            "Equity"
        )

        fd_df = forecast_fd(
            fd_opening,
            fd_monthly,
            fd_cagr,
            years,
            "FD"
        )

        bonds_df = forecast_asset(
            bonds_opening,
            bonds_monthly,
            bonds_cagr,
            years,
            "Bonds"
        )

        gold_df = forecast_asset(
            gold_opening,
            gold_monthly,
            gold_cagr,
            years,
            "Gold & Silver"
        )

        # ---------------------------------------------------
        # Total Corpus
        # ---------------------------------------------------

        total_corpus = (

            equity_df["Closing"].iloc[-1]
            +
            fd_df["Closing"].iloc[-1]
            +
            bonds_df["Closing"].iloc[-1]
            +
            gold_df["Closing"].iloc[-1]

        )

        adjusted_corpus = total_corpus * (1 - corpus_reduction)

        # ---------------------------------------------------
        # SWP Projection
        # ---------------------------------------------------

        swp_df = swp_forecast(

            corpus=adjusted_corpus,

            annual_return=growth_rate,

            annual_withdrawal=withdraw_amount,

            withdrawal_increase=withdraw_increase,

            max_years=100
        )

        # ---------------------------------------------------
        # Final Results
        # ---------------------------------------------------

        results = {

            "Equity Forecast":
                equity_df.to_dict(orient="records"),

            "FD Forecast":
                fd_df.to_dict(orient="records"),

            "Bonds Forecast":
                bonds_df.to_dict(orient="records"),

            "Gold Forecast":
                gold_df.to_dict(orient="records"),

            "SWP Forecast":
                swp_df.to_dict(orient="records")
        }

        return jsonify(results)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ---------------------------------------------------
# Main
# ---------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)