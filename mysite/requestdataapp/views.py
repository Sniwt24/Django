from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UploadFileForm
# Create your views here.

def error_view(request: HttpRequest) -> HttpResponse:
    dsc = request.GET.get("dsc", "")

    context = {
        "dsc": dsc,
    }
    return render(request, "requestdataapp/error.html", context)

def process_get_view(request: HttpRequest) -> HttpResponse:
    name = request.GET.get("name", "")
    firstname = request.GET.get("fname", "")
    context = {
        "name": name,
        "fname": firstname,
    }
    return render(request, "requestdataapp/request_query_params.html", context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:

    MSG = ""
    # if request.method == "POST" and request.FILES.get("myfile"):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES["myfile"]
            myfile = form.cleaned_data["file"]
            f_size = myfile.size / 1024 / 1024

            # if f_size > 1:
            #     MSG = f"File {myfile.name} is too big! It's size {f_size:.2f} MB"
            #     print("File was not saved, size ", myfile.size)
            # else:
            #     MSG = f"File {myfile.name} upload successfully! Size {f_size:.2f} MB"
            #     fs = FileSystemStorage()
            #     fs.location = fs.location + "/upload/"
            #     filename = fs.save(myfile.name, myfile)
            #     print(filename, "was saved, size ", myfile.size)

            MSG = f"File {myfile.name} upload successfully! Size {f_size:.2f} MB"
            fs = FileSystemStorage()
            fs.location = fs.location + "/upload/"
            filename = fs.save(myfile.name, myfile)
            print(filename, "was saved, size ", myfile.size)
    else:
        form = UploadFileForm()
        # print("Form is not valid! File was not save!")


    context = {
        "msg": MSG,
        "form": form,
    }
    return render(request, "requestdataapp/upload.html", context)
