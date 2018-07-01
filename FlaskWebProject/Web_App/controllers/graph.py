from flask import render_template, Blueprint
import pandas as pd
import pygal
from Web_App.sqlConnection import get_connections

graph_blueprint = Blueprint(
    'graph',
    __name__,
    template_folder='../templates/app/Graph')

@graph_blueprint.route('/StockGraph/<string:StockID>')
def StockGrpah(StockID):
    graph = pygal.Line()
    graph.title = 'Stock Graph for ' + StockID

    #Getting DB connection
    connection_string, engine, connection = get_connections()

    stock_query = "exec spMovingAverage @StockID= ? , @NumOfYears=2"
    stockResults =  pd.read_sql_query(stock_query,connection,params=[StockID])
    graph.x_labels = stockResults.StockPriceDate
    graph.add('Stock Price',  stockResults.StockClosePrice)
    graph.add('50 MA',  stockResults.Stock50MA)
    graph.add('200 MA',  stockResults.Stock200MA)
    graph_data = graph.render_data_uri()
    return render_template("lineGraph.html", graph_data = graph_data)
