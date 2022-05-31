from django.contrib import admin

# from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import *

# admin.site.register(Rubric, MPTTModelAdmin)
admin.site.register(Rubric, DraggableMPTTAdmin)
admin.site.register(Article)
