import streamlit as st
import yfinance as yf
import pandas as pd


def display_finviz_chart(ticker):
    """Displays Finviz chart for the given ticker.

    Args:
        ticker (str): A stock ticker symbol (e.g., "MSFT").
    """
    st.header("Finviz Chart Viewer")
    finviz_url = f"https://finviz.com/chart.ashx?t={ticker}&ty=c&ta=st_1,ta_4&p=d&s=l"  # Create finviz url
    st.markdown(f'<div style="text-align:center"><a href="{finviz_url}" target="_blank"><img src="{finviz_url}" style="width: 100%; border: 2px solid #cccccc; border-radius: 5px;"/></a></div>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center"><a href="{finviz_url}" target="_blank">{ticker}</a></p>', unsafe_allow_html=True)  # Place name of ticker below

def display_analyst_rating(ticker):
    """Displays Analyst rating for the given ticker.

    Args:
        ticker (str): A stock ticker symbol (e.g., "MSFT").
    """
    stock = yf.Ticker(ticker)
    rating = stock.recommendations
    if rating is not None:
        st.subheader("Analyst Rating")
        st.dataframe(rating.tail(10))  # Display the last 10 ratings
    else:
        st.write("No analyst rating available.")

def format_number(number):
    """Formats a large number into a more readable string."""
    if number is None:
        return "N/A"
    for unit in ['', 'K', 'M', 'B', 'T']:
        if abs(number) < 1000.0:
            return f"{number:3.1f}{unit}"
        number /= 1000.0
    return f"{number:.1f}T"

def format_percentage(number):
    """Formats a number into a percentage string."""
    if number is None:
        return "N/A"
    return f"{number * 100:.2f}%"

def format_pe_ratio(pe_ratio):
    """Formats the PE ratio with 2 decimals and adds the unit 'X'."""
    if pe_ratio is None:
        return "N/A"
    return f"{pe_ratio:.2f}X"

def display_stock_info(ticker):
    """Displays stock information for the given ticker.

    Args:
        ticker (str): A stock ticker symbol (e.g., "MSFT").
    """
    stock = yf.Ticker(ticker)
    info = stock.info
    st.subheader("Stock Information")
    st.write(f"**Market Cap:** {format_number(info.get('marketCap'))}")
    st.write(f"**PE Ratio:** {format_pe_ratio(info.get('trailingPE'))}")
    st.write(f"**Forward PE:** {format_pe_ratio(info.get('forwardPE'))}")
    st.write(f"**Expected EPS Growth:** {format_percentage(info.get('earningsGrowth'))}")
    
    st.write(f"**Revenue:** {format_number(info.get('totalRevenue'))}")
    st.write(f"**Income:** {format_number(info.get('netIncomeToCommon'))}")
    
    st.write(f"**Outstanding Shares:** {format_number(info.get('sharesOutstanding'))}")
    st.write(f"**Sector:** {info.get('sector', 'N/A')}")

def display_financials(ticker):
    """Displays financials for the given ticker.

    Args:
        ticker (str): A stock ticker symbol (e.g., "MSFT").
    """
    stock = yf.Ticker(ticker)
    financials = stock.financials.T
    financials.index = financials.index.year
    financials['Total Revenue'] = financials['Total Revenue'].apply(format_number)
    financials['Net Income'] = financials['Net Income'].apply(format_number)
    st.subheader("Financials")
    st.dataframe(financials[['Total Revenue', 'Net Income']])

def display_calendar_and_expectations(ticker):
    """Displays the calendar and earnings expectations for the given ticker.

    Args:
        ticker (str): A stock ticker symbol (e.g., "MSFT").
    """
    stock = yf.Ticker(ticker)
    calendar = pd.DataFrame(stock.calendar)
    earnings = stock.earnings
    quarterly_earnings = stock.quarterly_earnings

    # Apply format_number only to numeric columns
    numeric_cols = calendar.select_dtypes(include=['number']).columns
    calendar[numeric_cols] = calendar[numeric_cols].applymap(format_number)
    
    if earnings is not None and 'Revenue' in earnings.columns:
        earnings['Revenue'] = earnings['Revenue'].apply(format_number)
    if earnings is not None and 'Earnings' in earnings.columns:
        earnings['Earnings'] = earnings['Earnings'].apply(format_number)
    
    if quarterly_earnings is not None and 'Revenue' in quarterly_earnings.columns:
        quarterly_earnings['Revenue'] = quarterly_earnings['Revenue'].apply(format_number)
    if quarterly_earnings is not None and 'Earnings' in quarterly_earnings.columns:
        quarterly_earnings['Earnings'] = quarterly_earnings['Earnings'].apply(format_number)

    st.subheader("Calendar")
    st.dataframe(calendar)

   
    if earnings is not None:
        st.dataframe(earnings)
    if quarterly_earnings is not None:
        st.dataframe(quarterly_earnings)


if __name__ == "__main__":
    st.sidebar.title("Finviz Chart Viewer")
    tickers = st.sidebar.multiselect(
        "Select Ticker Symbols:", 
        ["AAPL", "MSFT", "NVDA", "AMZN", "GOOG", "META", "TSLA", "WMT", "LLY", "JPM", "V", "MA", "ORCL", "XOM", "COST", "NFLX", "HD", "PG", "JNJ", "BAC", "SAP", "CRM", "ASML", "KO", "CVX", "ACN", "MRK", "CSCO", "IBM", "NOVN", "NESN", "AXP", "MS", "LIN", "AZN", "MCD", "PEP", "DIS", "PM", "ADBE", "PLTR", "QCOM", "AMD", "HSBA", "CAT", "T", "VZ", "INTU", "BLK", "BKNG", "AMGN", "C", "PFE", "SHOP", "AMAT", "HON", "UBER", "ULVR", "SANO", "TTE", "BA", "FRA:AIR", "CMCSA", "DE", "SBUX", "PANW", "CDI", "NKE", "SPOT", "LMT", "RIO", "MU", "BHP", "BN", "CRWD", "UPS", "PYPL", "ZURN", "BUD", "BATS", "INTC", "ABNB", "MMM", "RACE", "MAR", "FTNT", "MDLZ", "BNP", "COIN", "GSK", "DELL", "MUV2", "TGT", "SNOW", "FDX", "SQ", "HOLN", "VOW", "INGA", "LULU", "BMW", "GM", "O", "NET", "HMC", "RBLX", "ENI", "LLOY", "SREN", "KMB", "LONN", "DAL", "VALE", "ALC", "GLEN", "F", "ENGI", "YUM", "PGHN", "DBK", "SIKA", "GIVN", "STLA", "KHC", "CCL", "GIS", "TTWO", "EBAY", "EA", "ZS", "KER", "EL", "TSCO", "BNTX", "SCMN", "K", "SCHN", "P911", "ZM", "PHIA", "WBD", "DTE", "KNIN", "LISN", "CHKP", "CBK", "RWE", "PINS", "EXPE", "VOD", "SLHN", "VIE", "SOON", "SNAP", "GEBN", "HEIO", "MONC", "SGSN", "EMSN", "VIV", "MRNA", "EDR", "RIVN", "NCLH", "ROKU", "AAL", "VACN", "ZAL", "UHR", "MTCH", "CFR", "ALO", "LCID", "HELN", "HAS", "BCVN", "SUN", "LHA", "BALN", "ALV", "MKS", "FHZN", "ETSY", "SQN", "CS", "TEMN", "MC", "OR", "ACA", "PUM", "ACLN", "EMMN", "BRBY", "TUI1", "AI", "BKW", "ORA", "BOSS", "UAA", "HOG", "RMS", "PTON", "TKA", "SGKN", "MANU", "GT", "ROSE", "BEKN", "CLN", "SRAIL", "BCGE", "FL", "MSGE", "PLUG", "VATN", "ROG", "NVAX", "JUVE", "BMBL", "ADEN", "HFG", "AC", "CAC", "IMPN", "BYND"], 
        default=["GOOG", "AMZN", "PLTR"]
    )   
    for ticker in tickers:
        st.write(f"## {ticker}")
        display_finviz_chart(ticker)
        display_stock_info(ticker)
        display_financials(ticker)
        display_calendar_and_expectations(ticker)
        display_analyst_rating(ticker)
        st.write("---")
    
    st.sidebar.write("Made with ❤️ by Manu")