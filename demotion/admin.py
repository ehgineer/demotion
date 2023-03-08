from django.contrib import admin
from .models import Image, Prediction, Interpretation


admin.site.register(Image)
admin.site.register(Prediction)
admin.site.register(Interpretation)