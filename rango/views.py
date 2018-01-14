from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	# dictionary will be passed to the template engine as its context
	context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
	# the render takes the user request, the index page, and the dictionary to produce an HTML page
	# which is then dispatched to the user's web browser
	return render(request, 'rango/index.html', context=context_dict)
	
def about(request):
	return render(request, 'rango/about.html')
	# below removed after completing chapter 4 exercise
	# return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
