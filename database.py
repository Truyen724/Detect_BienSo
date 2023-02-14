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
    print("loi 0")
    Id_parkinglot = get_parking_id(id_camera)
    print("loi 1")
    query = "Insert into Action(ID_action, ID_car, Image, Image2, In_or_out, Time,Id_parkinglot) values ({id_action},'{id_car}','{image1}','{image2}','{state}','{Time}','{Id_parkinglot}')".format(id_action=id_action,id_car = id_car,image1=image1,image2=image2,state=state,Time = Time, Id_parkinglot=Id_parkinglot)
    with engine.connect() as connection:
        connection.execute(text(query))
    print("loi 2")
    query_update = "update car set State = '{State}' where Id_car='{id_car}'".format(State = state, id_car = id_car)
    with engine.connect() as connection:
        connection.execute(text(query_update))
    print("loi 3")

def get_inout(id_car):
    state = "out"
    query = "SELECT top(1) In_or_out from action where id_car = '{id_car}' order by ID_action Desc".format(id_car= id_car)
    with engine.connect() as connection:
        result = connection.execute(text(query))
        if(result.rowcount!=0):
            for row in result:
                state = row["In_or_out"].replace(" ","")
        else:
            
            query2 = "SELECT state FROM car where Id_car = '{id_car}'".format(id_car= id_car)
            with engine.connect() as connection:
                result2 = connection.execute(text(query2))
                if(result2.rowcount!=0):
                    for row in result2:
                        state = row["state"].replace(" ","")
                else:
                    state = "out"
    if(state == "in"):
        state = "out"
    elif(state == "out"):
        state = "in"
    print("Xong phan nay")
    return state
def get_parking_id(id_camera):
    query = "select ID_parking_lot from Camera where ID_camera = '{id_camera}'".format(id_camera = id_camera)
    ID_parkinglot = "0"
    with engine.connect() as connection:
        result = connection.execute(text(query))
        if(result.rowcount!=0):
            for row in result:
                ID_parkinglot = row["ID_parking_lot"].replace(" ","")
    return ID_parkinglot
