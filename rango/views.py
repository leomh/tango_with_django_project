from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page


def index(request):
    # Query the database for a list of all categories  currently stored
    # Order the categories by no. likes in descending order
    # Retrieve the top 5 only - or all if less than 5
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine

    category_list = Category.objects.order_by('-likes')[:5]
    # Same thing for pages

    pages_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': pages_list}

    # Render the response
    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')
    # below removed after completing chapter 4 exercise
    # return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine
    context_dict = {}
    try:
        # Try to find a category name slug with the given name
        # Otherwise .get() raises a DoesNotExist exception
        # so .get() returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages
        # NB: filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        # Add our results list to the template context under name pages
        context_dict['pages'] = pages

        # Also add the category object from the db to the context dictionary
        # To be used in the template to verify that the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        # the template will display the "no category" message for us
        context_dict['category'] = None
        context_dict['pages'] = None

    # Render the response and return it
    return render(request, 'rango/category.html', context_dict)