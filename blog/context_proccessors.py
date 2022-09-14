from .models import Category


def navbar_context(request):
    """add the dropdown categories on all the views"""
    return {'cat_menu': Category.objects.all(), }
