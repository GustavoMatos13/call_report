from django.contrib import admin
from .models.callStart import CallStart
from .models.callEnd import CallEnd


# Register your models here.
admin.site.register(CallStart)
admin.site.register(CallEnd)
