from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=False)

    def __str__(self) -> str:
        return f"Author (pk={self.pk}, name={self.name!r})"


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self) -> str:
        return f"Category (pk={self.pk}, name={self.name!r})"


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"Tag (pk={self.pk}, name={self.name!r})"


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=False, blank=False)
    pub_date = models.DateTimeField(null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="articles")
