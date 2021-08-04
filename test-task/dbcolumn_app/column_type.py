import psycopg2

import numpy
import pandas as pd

from .raw_con_handle import db_hostName, db_portNumber, db_service_name, db_user, db_password


class DataType():
    permission_classes          = []
    authentication_classes      = []
     

    # Find get account type
    def data_type(tablenane, columnname):
        try:
            conn = psycopg2.connect(host=db_hostName,
                                    port=db_portNumber,
                                    database=db_service_name,
                                    user=db_user,
                                    password=db_password)
            cursor = conn.cursor()
            sql_query = "select data_type from information_schema.columns where table_name = %s and column_name = %s"
            data = (tablenane, columnname)
            cursor.execute(sql_query, data)
            data = cursor.fetchone()
            # print("Connection established to: ", data[0])

            #Closing the connection
        except:
            return "err"
        finally: 
            cursor.close()
            conn.close()
            
        return data[0]