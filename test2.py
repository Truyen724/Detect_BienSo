from sqlalchemy.engine import URL
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-O41267U;DATABASE=Detect_bienso;Trusted_Connection=yes"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

from sqlalchemy import create_engine
engine = create_engine(connection_url)

# import pandas as pd
# data = pd.read_sql_query("Insert into Driver(ID_driver, Driver_Name ,Dateofbirth) values ('5',N'Nguyễn Thị Tiểu Thuyết','19960714')", engine)
# print(data.head())
from sqlalchemy import text

with engine.connect() as connection:
    result = connection.execute(text("Insert into Driver(ID_driver, Driver_Name ,Dateofbirth) values ('5',N'Nguyễn Thị Tiểu Thuyết','19960714')"))
