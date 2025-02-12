import datetime
import yfinance as yf
import dash
from dash import dcc, html  # For Dash 2.x
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Stock Visualization Dashboard"

# Define the app layout: an input box, a search button, and a graph
app.layout = html.Div([
    html.H1("Stock Visualization Dashboard"),
    html.H4("Enter a stock symbol (e.g., AAPL, MSFT, TSLA)"),
    dcc.Input(id='input-stock', value='AAPL', type='text'),
    html.Button('Search', id='submit-button', n_clicks=0),
    dcc.Graph(id='stock-chart')
])

# Callback: Triggered by clicking the Search button
@app.callback(
    Output('stock-chart', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('input-stock', 'value')
)
def update_graph(n_clicks, stock_symbol):
    # Only run when the search button has been clicked
    if n_clicks == 0:
        # Return an empty figure until the button is clicked
        return {}

    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()

    # Fetch stock data using yfinance
    df = yf.download(stock_symbol, start=start, end=end)
    
    # If no data is found, return an empty figure
    if df.empty:
        return {}

    # Reset index so the date becomes a column
    df = df.reset_index()

    # Flatten the MultiIndex columns if necessary
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # Round the 'Close' column to two decimal places
    df['Close'] = df['Close'].round(2)

    # Create a line chart using Plotly Express
    fig = px.line(df, x='Date', y='Close', title=f'{stock_symbol} Stock Price')

    # Update layout to label axes and ensure x-axis is interpreted as dates
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis=dict(type='date')
    )

    return fig

# Run the Dash app on localhost
if __name__ == '__main__':
    app.run_server()
