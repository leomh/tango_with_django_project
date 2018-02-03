from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


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

@login_required
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

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


def register(request):
    # tells the template: was the registration successful?
    registered = False

    # if it's a HTTP POST, we will process form data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            # hash the password and then update the user object
            user.set_password(user.password)
            user.save()

            # commit=False delays saving the model until
            # we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST: render our form with blank forms ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        # get() will return None if the value does not exist instead of a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))