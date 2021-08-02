import json

import io

import xlrd
import os
import tempfile

import pandas as pd

from django.shortcuts import render

from django.db import connection
from django.apps import apps

from django.views.generic import CreateView
from django.http import HttpResponse

from .models import HouseHoldModel
from .forms import HouseHoldForm

# Create your views here.


class CreatePostView(CreateView): # new
    model = HouseHoldModel
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
        
        excel_raw_data_1 = pd.read_excel(request.FILES.get('filename'),'Sheet1')
        # excel_raw_data_1 = pd.read_excel(request.FILES.get('filename'))
        print("### Dataframe ####\n", excel_raw_data_1)

        selected_table = request.POST.get('table_name')
        print("selected table name: ", selected_table)

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

        # # Insert into model
        # insert_into_HouseHoldModel = HouseHoldModel(
        #     issue_maker                 = operating_user,
            
        # )
            
        # insert_into_HouseHoldModel.save()

        return render(request, "page.html")


##################################################
#### API
####################################################
class TableColumnFoundView(CreateView): # new
    model = HouseHoldModel
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
 
    