from sqlalchemy.engine import URL
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-O41267U;DATABASE=Detect_bienso;Trusted_Connection=yes"
connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
from sqlalchemy import text
from sqlalchemy import create_engine
engine = create_engine(connection_url)
import time
from datetime import datetime
def current_milli_time():
    return round(time.time() * 1000)
def add_action(id_car, image1, image2, id_camera):
    id_action = current_milli_time()
    now = datetime.now()
    Time = now.strftime("%d/%m/%Y %H:%M:%S")
    state = get_intout(id_car)
    query = "Insert into Action(ID_action, ID_car, Image, Image2, In_or_out, Time,Id_parkinglot) values"
def get_inout(id_car):
    state = "in"
    query = "SELECT top(1) In_or_out from action where id_car = '{id_car}' order by ID_action Desc".format(id_car= id_car)
    with engine.connect() as connection:
        result = connection.execute(text(query))
        if(result.rowcount!=0):
            for row in result:
                state = row["In_or_out"].replace(" ","")
        else:
            print("Khong có dữ liệu")
    if(state == "in"):
        state = "out"
    if(state == "out"):
        state = "in"
    return state
