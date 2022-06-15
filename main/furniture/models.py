from django.db import models
from django.urls import reverse

class Furniture(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Содержимое")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name= "Фото")
    time_create = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateField(auto_now=True,verbose_name="Время редактирования")
    is_published=models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,  verbose_name="Принадлежность к ассортименту")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs ={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Мебельная фабрика'
        verbose_name_plural = 'Мебельная фабрика'
        ordering = ['time_create','title']


class Category(models.Model):
        name = models.CharField(max_length=100, db_index=True, verbose_name='Ассортимент')
        slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

        def __str__(self):
            return self.name

        def get_absolute_url(self):
            return reverse('category', kwargs={'cat_slug': self.slug})

        class Meta:
            verbose_name ='Ассортимент'
            verbose_name_plural ='Ассортименты'
            ordering=['id']


class ExpertVoted(models.Model):
    user = models.CharField(max_length = 100)
    is_voted = models.BooleanField()

class ProductVote(models.Model):
    product1mark = models.IntegerField()
    product2mark = models.IntegerField()
    product3mark = models.IntegerField()

class Admincreatevote(models.Model):
    category1 = models.ForeignKey('Category', on_delete=models.PROTECT,  verbose_name="Принадлежность к ассортименту", related_name='category1')
    category2 = models.ForeignKey('Category', on_delete=models.PROTECT,  verbose_name="Принадлежность к ассортименту",related_name='category2')
    category3 = models.ForeignKey('Category', on_delete=models.PROTECT,  verbose_name="Принадлежность к ассортименту",related_name='category3')