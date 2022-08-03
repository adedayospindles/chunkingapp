from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from .models import File, User
import pandas as pd
from django.contrib import messages
import shutil
import os
import math
import json
import csv

# Create your views here.
# ******************* HOME VIEW *****************************
def homePage(request):
    if request.user.is_authenticated:
        user = request.user
        allfile = user.file_set.all()
        context = {"allfile": allfile}

        return render(request, "home.html", context)

    return render(request, "home.html") 


def splitCSV(request):
    if request.method == 'POST':
        file_data = request.FILES["file"]
        
        if file_data.name.split(".")[-1] not in ["json","csv"]:
            messages.error(request, "Please upload csv or json file")
            return redirect(request.META.get("HTTP_REFERER"))

        user_specified_size = request.POST["chunk_size"]
        user_specified_size = int(user_specified_size)
        file_name = default_storage.save(file_data.name, file_data)
        file_path = default_storage.path(file_name)

        if file_path.split(".")[-1] == 'csv':
            file= File.objects.create(user=request.user,uploaded_file=file_path)
            file_size = os.path.getsize(file_path)
            no_file_row = len(pd.read_csv(file_path)) - 1
            no_of_chuncked_file = math.ceil(file_size/user_specified_size)
            chunksize_user_specified_size = math.ceil(no_file_row/no_of_chuncked_file)
            folder_name = file_path.split(".")[0]
            os.makedirs(folder_name)
            index = 0
            for chunk in pd.read_csv(file_path, chunksize=chunksize_user_specified_size):
                chunk.to_csv(f"{folder_name}/file{index}.csv".format(index), index=False)
                index += 1

        if file_path.split(".")[-1] == 'json':
            file= File.objects.create(user=request.user,uploaded_file=file_path)
            file_size = os.path.getsize(file_path)
            folder_name = file_path.split(".")[0]
            size = math.ceil(file_size/user_specified_size)
            os.makedirs(folder_name)
            with open(file_path,'r') as infile:
                o = json.load(infile)
                index = 0
                for i in range(0, len(o), size):
                    with open(f"{folder_name}/file{index}.json".format(index), 'w') as outfile:
                        index += 1
                        json.dump(o[i:i+user_specified_size], outfile)


        fs = folder_name.split("\\")[-1]
        outputfile = str(settings.MEDIA_ROOT) + f"\\zipped-files\\{fs}"
           
        shutil.make_archive(outputfile, 'zip', folder_name)
        shutil.rmtree(folder_name)
        file.file_name = f"{fs}.zip"
        file.zip_file = f"/{outputfile}.zip"
        file.save()
        os.remove(file_path)
        context = {"file": file}
        return render(request, "splitcsv.html", context)
        
    return render(request, "splitcsv.html")



def save(request, pk):
    file = File.objects.get(id=pk)
    file.saved_file = file.zip_file
    file.save()
    return HttpResponse("File saved successsfully")

def delete(request, pk):
    file = File.objects.get(id=pk)
    file.delete()
    return HttpResponse("File deleted successsfully")

# ******************* DOWNLOAD VIEW *****************************
# def download(request, pk):
#     file = File.objects.filter(id=pk).first()
#     name = file.file_name
#     response = HttpResponse(open(str(settings.MEDIA_ROOT) + f"\\zipped-files\\{name}.zip", 'rb'), content_type='application/zip')
#     response['Content-Disposition'] = "inline;file-name="+f"{name}.zip"
#     return response

# def download(request, pk):
#     file = File.objects.filter(id=pk).first()
    


# def download(request):
#     response = HttpResponse(open(f"media/books.zip", 'rb'), content_type='application/zip')
#     response['Content-Disposition'] = "inline;file-name=books.csv"
#     return response


def csvToJson(request):
    if request.method == "POST":
        csv_file = request.FILES["CSVfile"]
        json_file_name = csv_file.name.split(".")[0] + "-json-file.json"
        file_name = default_storage.save(csv_file.name, csv_file)
        file_path = default_storage.path(file_name)
        json_array= []
        
        json_path = f"{settings.MEDIA_ROOT}/{json_file_name}"
        with open(file_path, encoding="utf-8") as csv_file_handler:
            csv_reader = csv.DictReader(csv_file_handler)
            for rows in csv_reader:
                json_array.append(rows)
        with open(json_path, 'w', encoding="utf-8") as json_file_handler:
            json_file_handler.write(json.dumps(json_array, indent=4))
        json_file = json_path.split("/")[-1]
        file = File.objects.create(user=request.user, file_name=json_file_name, zip_file=json_file)
        file.save()
        os.remove(file_path)
        context = {"file": file}
        return render(request, "csvToJson.html", context)
    context = {}
    return render(request, "csvToJson.html", context)


def jsonToCsv(request):
    return HttpResponse("Under construction")