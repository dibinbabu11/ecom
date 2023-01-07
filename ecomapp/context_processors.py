from . models import category

def menu_links(requests):
    links=category.objects.all()
    return dict(links=links)