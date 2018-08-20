from flask import render_template
from . import graph_blueprint
import pandas as pd
import pygal
from Web_App.sqlConnection import get_connections
from flask_login import login_required, current_user

@graph_blueprint.route('/StockGraph/<string:StockID>')
@login_required
def StockGrpah(StockID):
    graph = pygal.Line()
    graph.title = 'Stock Graph for ' + StockID

    #Getting DB connection
    connection_string, engine, connection = get_connections()

    #Stock Graph
    stock_query = "exec spMovingAverage @StockID= ? , @NumOfYears=2"
    stockResults =  pd.read_sql_query(stock_query,connection,params=[StockID])
    graph.x_labels = stockResults.StockPriceDate
    graph.add('Stock Price',  stockResults.StockClosePrice)
    graph.add('50 MA',  stockResults.Stock50MA)
    graph.add('200 MA',  stockResults.Stock200MA)
    graph_data = graph.render_data_uri()
    
    #Bollinger_Band_graph
    graph_bb = pygal.Line()
    graph_bb.title = 'Bollinger Band for ' + StockID
    stock_query = "exec spBollingerBands @StockID= ? , @NumOfYears=3"
    stockResults =  pd.read_sql_query(stock_query,connection,params=[StockID])
    graph_bb.x_labels = stockResults.StockPriceDate
    graph_bb.add('Stock Price',  stockResults.StockClosePrice)
    graph_bb.add('50 MA',  stockResults.MA50)
    graph_bb.add('Upper Bound',  stockResults.UpperBollinger)
    graph_bb.add('Lower Bound',  stockResults.LowerBollinger)
    Bollinger_Band_graph = graph_bb.render_data_uri()
    return render_template("app/graph/lineGraph.html", graph_data = graph_data, Bollinger_Band_graph = Bollinger_Band_graph)
