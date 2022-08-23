from .models import Category

def navbar_context(request):
    return {'cat_menu': Category.objects.all(), }
