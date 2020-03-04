import mysql.connector

def mysql_Program(Value):
    try:
        connection_config_Dict = {
            # 'host'              :"192.168.5.4",
            'host'              :"127.0.0.1",
            'port'              :"3307",
            'user'              :"Ground_Nusa",
            'password'          :"groundnusa",
            'database'          :"ground_nusa",
            'use_pure'          : False,
            'raise_on_warnings' : True,
            'autocommit'        : True}
        connection = mysql.connector.connect(**connection_config_Dict)
        
        mySQL_Create_Main_Table = """CREATE TABLE IF NOT EXISTS Log (
            ID int AUTO_INCREMENT,
            Date_Log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Mouse_Value int NOT NULL,
            PRIMARY KEY (ID))"""
        
        # mySQL_Input_Data = """INSERT INTO Log (Mouse_Value)
        # VALUES
        # (%s)"""
        # params = (Value)
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server Version", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ",record)
            # create_table = cursor.execute(mySQL_Create_Main_Table)
            
            # if (Condition == 1):
            cursor.execute("INSERT INTO log (Mouse_Value) VALUES (%s)", (Value,))
            print("Data Inputed")
            # else(Condition == 2):
            #     sql_all_query = "SELECT * FROM Log"
            #     cursor.execute(sql_all_query)
            #     record = cursor.fetchall()
            #     lastrecord = cursor.rowcount-1
                
            #     Date = record[lastrecord[1]]
            #     return Date

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

