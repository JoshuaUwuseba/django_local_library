from django.shortcuts import render, redirect, render_to_response
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def register(request):
    if request.method == "POST":
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, "Account created successfully")
            username = f.cleaned_data.get('username')
            password = f.cleaned_data.get('password2')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('register')
    else:
        f = CustomUserCreationForm()

    return render(request, "register.html", {"form": f})

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

    return render_to_response('login.html', context_instance=RequestContext(request))


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances': num_instances,
        'num_instance_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits, 
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    paginate_by = 1
   
class BookDetailView(generic.DetailView):
    model = Book
    
class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')