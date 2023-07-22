from django.contrib import admin

# Register your models here.
from .models import Categoria, Producto

#admin.site.register(Categoria)
#admin.site.register(Producto)
@admin.register(Categoria)
class Categoriaadmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_registro')

@admin.register(Producto)
class Productoadmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'categoria')
    #list_editable = ('precio',)