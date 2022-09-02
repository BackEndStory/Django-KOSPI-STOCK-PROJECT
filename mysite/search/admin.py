from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Stockname_stocks, Document




admin.site.register(Stockname_stocks)
admin.site.register(Document)