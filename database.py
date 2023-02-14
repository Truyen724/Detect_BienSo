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
    state = get_inout(id_car)
    Id_parkinglot = get_parking_id(id_camera)
    query = "Insert into Action(ID_action, ID_car, Image, Image2, In_or_out, Time,Id_parkinglot) values ({id_action},'{id_car}','{image1}','{image2}','{state}','{Time}','{Id_parkinglot}')".format(id_action=id_action,id_car = id_car,image1=image1,image2=image2,state=state,Time = Time, Id_parkinglot=Id_parkinglot)
    query_update = "update car set State = '{State}' where Id_car='{id_car}'".format(State = state, id_car = id_car)
    with engine.connect() as connection:
        result = connection.execute(text(query))
        connection.execute(text(query_update))

def get_inout(id_car):
    state = "out"
    query = "SELECT top(1) In_or_out from action where id_car = '{id_car}' order by ID_action Desc".format(id_car= id_car)
    with engine.connect() as connection:
        result = connection.execute(text(query))
        if(result.rowcount!=0):
            for row in result:
                state = row["In_or_out"].replace(" ","")
        else:
            print("Khong có dữ liệu")
            query2 = "SELECT state FROM "
            with engine.connect() as connection:
                result = connection.execute(text(query2))
    if(state == "in"):
        state = "out"
    if(state == "out"):
        state = "in"
    return state
def get_parking_id(id_camera):
    query = "select ID_parking_lot from Camera where ID_camera = '{id_camera}'".format(id_camera = id_camera)
    with engine.connect() as connection:
        result = connection.execute(text(query))
        if(result.rowcount!=0):
            for row in result:
                ID_parkinglot = row["ID_parking_lot"].replace(" ","")
    return ID_parkinglot
