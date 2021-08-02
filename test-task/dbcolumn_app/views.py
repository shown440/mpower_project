import json

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
        print("Table Info: ", table_info)

        return render(request, "page.html", {"tables_name": tables_name,
                                            "tables_column_d": tables_column_d}) 
 
    def post(self, request):
        

        data                    = request.POST
        print("########### ", data) 

        

        # Insert into model
        insert_into_HouseHoldModel = HouseHoldModel(
            issue_maker                 = operating_user,
            
        )
            
        insert_into_HouseHoldModel.save()

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

        table_columns = tables_column_d[mytable]
        print("Table Info: ", table_columns)
        # json_data = {table: str(table_columns)}
        json_data = {"response": table_columns}

        return HttpResponse(json.dumps(json_data), content_type="application/json")  
 
    