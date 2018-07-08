import pyodbc
import sys
import sqlalchemy as sq
import pandas as pd
import os

def get_sql_connection(svr,db,user,psw):

    server = svr + '.database.windows.net'
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1443;DATABASE='+db+';UID='+user+';PWD='+ psw)
    return cnxn

def get_all_sql_connection(svr,db,user,psw):
    connection_string = get_sql_connection_string(svr,db,user,psw) #os.environ.get('SQL_ConnectionString')
    engine = sq.engine.create_engine(connection_string)
    connection = engine.connect()
    return connection_string, engine, connection

def get_sql_connection_string(svr,db,user,psw):
    driver= 'ODBC+Driver+13+for+SQL+Server'
    connection_string = 'mssql+pyodbc://'+user+'@'+svr+':'+psw+'@'+svr+'.database.windows.net:1433/'+db+'?driver='+driver+';'
    return connection_string
    
def get_connections():
    return get_all_sql_connection(svr=os.environ.get('CC_SVR'),db=os.environ.get('CC_SVR'),user=os.environ.get('CC_USER'),psw=os.environ.get('CC_PSW'))

if __name__ == "__main__":
    svr = sys.argv[1]
    db = sys.argv[2]
    user = sys.argv[3]
    psw = sys.argv[4]
    connection_string, engine, cnxn = get_all_sql_connection(svr,db,user,psw)
    query = "SELECT StockPriceDate,StockPriceYear,StockPriceMonth,StockOpenPrice,StockLowPrice, \
                StockHighPrice,StockClosePrice,DailyChangePricePerc,StockPriceChangeGroup \
                FROM [CoveredCalls].[dbo].vStockHistory WHERE StockID= ?  and StockPriceDate>= ? "
    pd1 = pd.read_sql_query(query,cnxn,params=('X','2018-01-01'),index_col="StockPriceDate",
                             parse_dates=True)
    print(pd1)
    #connection = get_alchemy_connection(svr,db,user,psw)