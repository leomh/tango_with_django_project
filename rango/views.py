from django.shortcuts import render
#from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm


def index(request):
    # Query the database for a list of all categories  currently stored
    # Order the categories by no. likes in descending order
    # Retrieve the top 5 only - or all if less than 5
    # Place the list in our context_dict dictionary
    # that will be passed to the template engine

    category_list = Category.objects.order_by('-likes')[:5]
    # Same thing for pages

    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

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

def add_category(request):
    # three scenarios:
    # showing a new blank form for adding a category
    # saving a form data provided by the user to the associated model,
    # and rendering the Rango homepage
    # if there are errors, redisplay the form with them
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # check for valid form
        if form.is_valid():
            # Save the new category to the db
            category = form.save(commit=True)
            # We direct the user back to the index page
            # because the most recent category added is on the index page
            # print confirmation that the category has been added
            print (category, category.slug)
            return index(request)
        else:
            # print errors contained in the form to the terminal
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases
    # Render the form with any error messages
    return render(request, 'rango/add_category.html', {'form': form})