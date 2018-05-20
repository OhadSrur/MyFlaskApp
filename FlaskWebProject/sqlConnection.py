import pyodbc
import sys
import sqlalchemy as sq
import pandas as pd

def get_sql_connection(svr,db,user,psw):

    server = svr + '.database.windows.net'
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+db+';UID='+user+';PWD='+ psw)
    return cnxn

def get_sql_engine(svr,db,user,psw):
    driver= 'ODBC+Driver+13+for+SQL+Server'
    connection_string = 'mssql+pyodbc://'+user+'@'+db+':'+psw+'@'+svr+':1433/CoveredCalls?driver='+driver+';'
    engine = sq.engine.create_engine(connection_string)
    engine.connect()
    return engine

def get_alchemy_connection(svr,db,user,psw):
    engine = get_sql_engine(svr,db,user,psw)
    connection = engine.connect()
    return connection

if __name__ == "__main__":
    svr = sys.argv[1]
    db = sys.argv[2]
    user = sys.argv[3]
    psw = sys.argv[4]
    cnxn = get_sql_connection(svr,db,user,psw)
    query = "SELECT StockPriceDate,StockPriceYear,StockPriceMonth,StockOpenPrice,StockLowPrice, \
                StockHighPrice,StockClosePrice,DailyChangePricePerc,StockPriceChangeGroup \
                FROM [CoveredCalls].[dbo].vStockHistory WHERE StockID= ?  and StockPriceDate>= ? "
    pd1 = pd.read_sql_query(query,cnxn,params=('X','2018-01-01'),index_col="StockPriceDate",
                             parse_dates=True)
    print(pd1)
    #connection = get_alchemy_connection(svr,db,user,psw)