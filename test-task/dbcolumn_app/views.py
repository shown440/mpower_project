import json

import io

# import xlrd
# import os
# import tempfile

import psycopg2

import numpy
import pandas as pd

from django.shortcuts import render

from django.db import connection
from django.apps import apps

from django.views.generic import CreateView
from django.http import HttpResponse

from .models import HOUSEHOLDModel
from .forms import HouseHoldForm

from .column_type import DataType

from .raw_con_handle import db_hostName, db_portNumber, db_service_name, db_user, db_password

# Create your views here.


class CreatePostView(CreateView): # new
    model = HOUSEHOLDModel
    form_class = HouseHoldForm
    template_name = 'page.html' 


    def get(self, request):
        
        tables_name = connection.introspection.table_names()
        # tables_columns = connection.introspection.table_names().columns
        # seen_models = connection.introspection.installed_models(tables_name)
        # print("Tables name: ", tables_name)

        table_info = []
        tables_column_d = {}
        for model in apps.get_models():
            if model._meta.proxy:
                continue

            table = model._meta.db_table
            if table not in tables_name:
                continue

            columns = [field.column for field in model._meta.fields]
            table_info.append((table, columns))
            tables_column_d[table] = columns

        # print("Table Info: ", tables_column_d["HOUSEHOLD"])
        # print("Table Info: ", table_info)

        return render(request, "page.html", {"tables_name": tables_name,
                                            "tables_column_d": tables_column_d}) 
 
    def post(self, request):
        data                    = request.POST
        print("########### ", data) 
        
        excel_raw_df = pd.read_excel(r'E:\Office-Works\mPower\git-repository\test-task\dbcolumn_app\dataupload.xlsx','Sheet1')
        # excel_raw_df = pd.read_excel(request.FILES.get('filename'),'Sheet1')
        # excel_raw_data_1 = pd.read_excel(request.FILES.get('filename'))
        print("### Dataframe ####\n", excel_raw_df)
        df_columns = excel_raw_df.columns.values.tolist()
        df_columns.sort()
        print("DF columns: ", df_columns)
        with open(r'E:\Office-Works\mPower\git-repository\test-task\dbcolumn_app\tablejson.json') as jf:
            selected_tab_json = json.load(jf)
        selected_tab_keys = list(selected_tab_json.keys())
        selected_table = selected_tab_keys[0]
        # selected_table = request.POST.get('table_name')
        print("selected table name: ", selected_table)
        print("selected table map: ", selected_tab_json)
        tables_name = connection.introspection.table_names() 
        tables_column_d = {}
        for model in apps.get_models():
            if model._meta.proxy:
                continue
            table = model._meta.db_table
            if table not in tables_name:
                continue
            columns = [field.column for field in model._meta.fields] 
            tables_column_d[table] = columns
        table_columns = tables_column_d[selected_table]
        table_columns.remove('id')
        table_columns.sort()
        print("selected table column: ", table_columns)
        
        #############################################################################
        ##### automation with back end
        ##############################################################################
        print(">>>>>>>>: ", selected_tab_json[selected_table][0])
        source_col = []
        desti_col = []
        if set(df_columns).issubset(set(table_columns)):
            for i in range(0, len(selected_tab_json[selected_table])):
                source_col.append(selected_tab_json[selected_table][i]["source_column"])
                desti_col.append(selected_tab_json[selected_table][i]["destination_column"])
            print("Source col: ", source_col)
            print("Destination col: ", desti_col)

            json_list = []
            
            # json_formatting = excel_raw_df.to_dict()

            # for key in range(0, len(json_formatting.keys))
            # for i in excel_raw_df.index:
            for index, row in excel_raw_df.iterrows():
                json_formatting = {}
                # print("******: ",row['hh_head'], " ", row['hh_gender'], " ", row['hh_age'])
                # print("******: ",row)
                for sc in range(0, len(source_col)):
                    json_formatting[source_col[sc]] = row[source_col[sc]] 
                    # print("###: ", source_col[sc])
            #         json_formatting[source_col[sc]] = row[source_col[sc]] 
                # print("json dict \n",json_formatting)
                json_list.append(json_formatting) 
                # print("json list \n",json_list)
            print("json list final \n",json_list) 

            for dictionary in range(0, len(json_list)): 
                keys = list(json_list[dictionary].keys())
                print("dict keys: ", keys)
                
                insert_col = 'INSERT INTO public."'+selected_table+'"('
                insert_val = ' VALUES ('
                insert_data = []
                for key in range(0, len(keys)):
                    print("###### key: ",keys[key])
                    print("###### value: ",json_list[dictionary][keys[key]])
                    # print("######: ",isinstance(json_list[dictionary][keys[key]], numpy.int64))
                    
                    col_data_type = DataType.data_type(selected_table, keys[key])
                    print("Connection established to: ", col_data_type)
                    # print("Connection established type: ", type(col_data_type))

                    if col_data_type == "boolean":
                        try:
                            print("+++++++ Date type", json_list[dictionary][keys[key]])
                            print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
                            json_list[dictionary][keys[key]] = bool(json_list[dictionary][keys[key]])
                        except:
                            print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
                            msg = json_list[dictionary][keys[key]]+" is not boolean value."
                            return render(request, "page.html", {"msg": msg})
                    elif col_data_type == "integer":
                        try:
                            print("+++++++ Date type", json_list[dictionary][keys[key]])
                            print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
                            json_list[dictionary][keys[key]] = int(json_list[dictionary][keys[key]])
                        except:
                            print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
                            msg = json_list[dictionary][keys[key]]+" is not integer value."
                            return render(request, "page.html", {"msg": msg}) 
                    elif col_data_type == "timestamp with time zone":
                        try:
                            print("+++++++ Date type", json_list[dictionary][keys[key]])
                            print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
                            json_list[dictionary][keys[key]] = str(json_list[dictionary][keys[key]])
                            print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
                        except:
                            print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
                            msg = json_list[dictionary][keys[key]]+" is not date time value."
                            return render(request, "page.html", {"msg": msg})
                    elif col_data_type == "character varying":
                        try:
                            print("+++++++ Date type", json_list[dictionary][keys[key]])
                            print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
                            json_list[dictionary][keys[key]] = str(json_list[dictionary][keys[key]])
                        except:
                            print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
                            msg = json_list[dictionary][keys[key]]+" is not string value."
                            return render(request, "page.html", {"msg": msg})


                    # '''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) VALUES ('Ramya', 'Rama priya', 27, 'F', 9000)'''
                    insert_col+=keys[key]
                    if key == len(keys)-1:
                        insert_col+=')'
                    else:
                        insert_col+=','
                    
                    insert_val+='%s'
                    if key == len(keys)-1:
                        insert_val+=')'
                    else:
                        insert_val+=','

                    insert_data.append(json_list[dictionary][keys[key]])
                    
                insert_data = tuple(insert_data)
                print("****: ",insert_col,insert_val)
                print("**** data list: ",insert_data)
                try:
                    conn = psycopg2.connect(host=db_hostName,
                                            port=db_portNumber,
                                            database=db_service_name,
                                            user=db_user,
                                            password=db_password)
                    #Setting auto commit false
                    conn.autocommit = True      
                    cursor = conn.cursor()
                    sql_query = insert_col+insert_val 
                    cursor.execute(sql_query, insert_data)
                    conn.commit()
                    print("..........Records inserted........")  
                finally: 
                    cursor.close()
                    conn.close()   
                # break
            return render(request, "page.html")
        else:
            msg = "Selected table and Excel files value are not match"
            return render(request, "page.html", {"msg": msg})

        #############################################################################
        ##### automation with front end
        ##############################################################################
        
        # json_list = []
        # json_formatting = {}

        # print("indexes: ",list(excel_raw_df.index))
        # print("exact df \n",excel_raw_df)
        # if df_columns in table_columns:
        #     for i in list(excel_raw_df.index):
        #         for col in range(0, len(df_columns)):
        #             json_formatting[df_columns[col]] = excel_raw_df[df_columns[col]][i]
        #         # table_columns[i] = excel_raw_df[table_columns[i]]
        #         # print(df['Name'][i], df['Stream'][i])
        #         json_list.append(json_formatting)
        #     print("json list \n",json_list)
        #     # print("Table column and xlsx columns are match")

        #     for dictionary in range(0, len(json_list)): 
        #         keys = list(json_list[dictionary].keys())
        #         print("dict keys: ", keys)
                
        #         insert_col = 'INSERT INTO public."'+selected_table+'"('
        #         insert_val = ' VALUES ('
        #         insert_data = []
        #         for key in range(0, len(keys)):
        #             print("###### key: ",keys[key])
        #             print("###### value: ",json_list[dictionary][keys[key]])
        #             # print("######: ",isinstance(json_list[dictionary][keys[key]], numpy.int64))
                    
        #             col_data_type = DataType.data_type(selected_table, keys[key])
        #             print("Connection established to: ", col_data_type)
        #             # print("Connection established type: ", type(col_data_type))

        #             if col_data_type == "boolean":
        #                 try:
        #                     print("+++++++ Date type", json_list[dictionary][keys[key]])
        #                     print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
        #                     json_list[dictionary][keys[key]] = bool(json_list[dictionary][keys[key]])
        #                 except:
        #                     print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
        #                     msg = json_list[dictionary][keys[key]]+" is not boolean value."
        #                     return render(request, "page.html", {"msg": msg})
        #             elif col_data_type == "integer":
        #                 try:
        #                     print("+++++++ Date type", json_list[dictionary][keys[key]])
        #                     print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
        #                     json_list[dictionary][keys[key]] = int(json_list[dictionary][keys[key]])
        #                 except:
        #                     print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
        #                     msg = json_list[dictionary][keys[key]]+" is not integer value."
        #                     return render(request, "page.html", {"msg": msg}) 
        #             elif col_data_type == "timestamp with time zone":
        #                 try:
        #                     print("+++++++ Date type", json_list[dictionary][keys[key]])
        #                     print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
        #                     json_list[dictionary][keys[key]] = str(json_list[dictionary][keys[key]])
        #                     print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
        #                 except:
        #                     print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
        #                     msg = json_list[dictionary][keys[key]]+" is not date time value."
        #                     return render(request, "page.html", {"msg": msg})
        #             elif col_data_type == "character varying":
        #                 try:
        #                     print("+++++++ Date type", json_list[dictionary][keys[key]])
        #                     print("+++++++ Date type", type(json_list[dictionary][keys[key]]))
        #                     json_list[dictionary][keys[key]] = str(json_list[dictionary][keys[key]])
        #                 except:
        #                     print("^^^^^^^^^^^^ Exception occur ^^^^^^^^^^^^^^")
        #                     msg = json_list[dictionary][keys[key]]+" is not string value."
        #                     return render(request, "page.html", {"msg": msg})


        #             # '''INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) VALUES ('Ramya', 'Rama priya', 27, 'F', 9000)'''
        #             insert_col+=keys[key]
        #             if key == len(keys)-1:
        #                 insert_col+=')'
        #             else:
        #                 insert_col+=','
                    
        #             insert_val+='%s'
        #             if key == len(keys)-1:
        #                 insert_val+=')'
        #             else:
        #                 insert_val+=','

        #             insert_data.append(json_list[dictionary][keys[key]])
                    
        #         insert_data = tuple(insert_data)
        #         print("****: ",insert_col,insert_val)
        #         print("**** data list: ",insert_data)
        #         try:
        #             conn = psycopg2.connect(host=db_hostName,
        #                                     port=db_portNumber,
        #                                     database=db_service_name,
        #                                     user=db_user,
        #                                     password=db_password)
        #             #Setting auto commit false
        #             # conn.autocommit = True      
        #             cursor = conn.cursor()
        #             sql_query = insert_col+insert_val 
        #             cursor.execute(sql_query, insert_data)
        #             # conn.commit()
        #             print("..........Records inserted........")  
        #         finally: 
        #             cursor.close()
        #             conn.close()   
                # break
        #     return render(request, "page.html")
        # else:
        #     msg = "Selected table and Excel files value are not match"
        #     return render(request, "page.html", {"msg": msg})
        
        
        
        
        # Insert into model
        # insert_into_HOUSEHOLDModel = HOUSEHOLDModel(
        #     issue_maker                 = operating_user,
            
        # )
            
        # insert_into_HOUSEHOLDModel.save()


        # input_file = request.FILES.get('filename')
        # wb = xlrd.open_workbook(filename=None, file_contents=input_file.read())

        # files               = request.FILES
        # xlxs_file       = files["filename"]
        # print("files: ", type(xlxs_file.read())) # .read()

        # myfilename = files["filename"].filename
        # with open(myfilename, 'wb') as f:  # Save the file locally
        #     f.write(form['myfile'].file.read())
        # df = pd.read_excel(myfilename)

        # toread = io.BytesIO()
        # toread.write(xlxs_file.read()) 
        # toread.seek(0) 

        # df = pd.read_excel(toread)
        # print(df.show())

        

        # return render(request, "page.html")


##################################################
#### API
####################################################
class TableColumnFoundView(CreateView): # new
    model = HOUSEHOLDModel
    form_class = HouseHoldForm
    template_name = 'page.html' 


    def get(self, request, mytable):
        
        tables_name = connection.introspection.table_names() 
        # print("Tables name: ", tables_name)
        # print("***",request)

        # table_info = []
        tables_column_d = {}
        for model in apps.get_models():
            if model._meta.proxy:
                continue

            table = model._meta.db_table
            if table not in tables_name:
                continue

            columns = [field.column for field in model._meta.fields]
            # table_info.append((table, columns))
            tables_column_d[table] = columns

        table_columns = tables_column_d[mytable]
        # print("Table Info: ", table_columns)
        # json_data = {table: str(table_columns)}
        json_data = {"response": table_columns}

        return HttpResponse(json.dumps(json_data), content_type="application/json")  
 
    