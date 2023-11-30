from django import forms
# imports for validation
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile


def validate_file_size(file: InMemoryUploadedFile) -> None:
    if file.name:
        f_size = file.size / 1024 / 1024
        if f_size > 1:
            MSG = f"File {file.name} is too big! It's size {f_size:.2f} MB! Must be less then 1 MB!"
            print("File was not saved, size ", file.size)
            raise ValidationError(MSG)
    else:
        raise ValidationError("File name error!")

class UploadFileForm(forms.Form):
    file = forms.FileField(label="Choose file:", validators=[validate_file_size])
