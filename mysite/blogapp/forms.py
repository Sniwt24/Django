from django.forms import ModelForm, SelectDateWidget

from blogapp.models import Article


class CreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = "title", "content", "pub_date", "author", "category", "tags"
        widgets = {
            "pub_date": SelectDateWidget(years=range(1900, 3000))
        }
