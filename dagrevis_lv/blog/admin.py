from django.contrib import admin

import models


admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
