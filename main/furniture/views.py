import json

from django.contrib.auth import logout, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *
def login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
@login_required
def sortfurniture(request, sort_slug):
    furniture = Furniture.objects.order_by(sort_slug)
    return render(request, 'base.html', {'furniture': furniture})

class FurnitureHome(DataMixin, ListView):
    model = Furniture
    template_name = 'furniture/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))
    def get_queryset(self):
        return Furniture.objects.filter(is_published=True)

#def index(request): #
#   posts = Furniture.objects.all()
#    cats = Category.objects.all()
#
#   context = {
#        'posts': posts,
#        'menu': menu,
#        'cats':cats,
#        'title':'Главная страница',
#        'cat_selected': 0,
#    }
#return render(request,'furniture/index.html', context=context)


def about(request):
    return render(request, 'furniture/about.html',  {'menu': menu, 'title':'О сайте'})

class AddPage( LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'furniture/add.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True


    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = "Добавление записи")
        return dict(list(context.items())+list(c_def.items()))

#def addpage(request):
#    if request.method == 'POST':
#        form = AddPostForm(request.POST)
#        if form.is_valid():
#           print(form.cleaned_data)
#    else:
#        form = AddPostForm()
#    return render(request, 'furniture/add.html', {'form':form, 'menu':menu, 'title':'Добавить заказ'})



def contact(request):
    return HttpResponse("Обратная связь")
#def login(request):
#    return HttpResponse('авторизация')
def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
def Adminpanel(request):
    return redirect('admin')

#def show_post(request, post_slug):
#    post = get_object_or_404(Furniture, slug=post_slug)

#    context ={
#        'post':post,
#        'menu': menu,
#        'title':post.title,
#        'cat_selected': post.cat_id,
#    }
#    return render(request, 'furniture/post.html',context=context )

class ShowPost(DataMixin,DetailView):
    model = Furniture
    template_name = 'furniture/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class FurnitureCategory(DataMixin,ListView):
    model = Furniture
    template_name = 'furniture/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Furniture.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Ассортимент - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
     form_class = UserCreationForm
     template_name = 'furniture/register.html'
     success_url = reverse_lazy('login')

     def get_context_data(self, *, object_list=None, **kwargs):
         context = super().get_context_data(**kwargs)
         c_def = self.get_user_context(title="Регистрация")
         return dict(list(context.items())+list(c_def.items()))

     def form_valid(self, form):
         user = form.save()
         login(self.request, user)
         user1 = user.username
         is_voted = False
         vote = ExpertVoted.objects.create(user=user1, is_voted=is_voted)
         vote.save()
         return redirect('home')



class LoginUser(DataMixin, LoginView):
     form_class = AuthenticationForm
     template_name='furniture/login.html'

     def get_context_data(self, *, object_list=None, **kwargs):
         context = super().get_context_data(**kwargs)
         c_def = self.get_user_context(title="Авторизация")
         return dict(list(context.items())+list(c_def.items()))

    # def get_success_url(self):
     #    return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')





def expertmark(request):
    if request.method == 'POST':
        product1mark = request.POST['product1mark']
        product2mark = request.POST['product2mark']
        product3mark = request.POST['product3mark']
        products = ProductVote.objects.create(product1mark=product1mark, product2mark=product2mark,product3mark=product3mark,)
        products.save()


        return redirect('/')
    else:
        cats = Admincreatevote.objects.all()
        form = ExpertForm()
        return render (request, 'expertmark.html', {'form':form, 'cats':cats})

def expertresult(request):
    a = 0
    result1 = 0
    result2 = 0
    result3 = 0
    products = ProductVote.objects.all()
    pr = Furniture.objects.all()
    for product in products:
        result1 += product.product1mark
        result2 += product.product2mark
        result3 += product.product3mark
        a += 1
    result1 = result1/a
    result2 = result2/a
    result3 = result3/a
    if result1 > result2 and result1 > result3:
        prname = pr[0].cat
        result = result1
    elif result2 > result1 and result2 >result3:
        prname = pr[1].cat
        result = result2
    else:
        prname = pr[2].cat
        result = result3
    data ={'prname':prname,'result':result}
    return render (request, 'result.html', data)

arr = []
i = [0,1]

@login_required(login_url='login')
def grade(request):
    catAmount= Category.objects.count()
    cats = Category.objects.all()
    if request.method =="POST":
        cell = request.POST["grade"]
        cell = int(cell)
        arr[i[0]] = cell
        i[0]= i[0] + 1
        if i[0]==catAmount:
            jackson = json.dumps(arr, indent=4)
            user = request.user.username
            grades = Grades.objects.create(chargrade = jackson, user = user)
            gr = Grades.objects.all()
            for g in gr:
                if user == g.user:
                    g.delete()
            grades.save()
            return redirect('home')
        cat1 = cats[i[0]]
        form = GradeForm()
        data = {'form':form, 'cat':cat1}
        return render(request, 'grade.html', context=data)
    else:
        arr.clear()
        i[0] = 0

        for jj in range(catAmount):
            arr.append(-1)
        cat1 = cats[i[0]]
        form = GradeForm()
        data = {'form':form, 'cat':cat1}
        return render(request, 'grade.html',context=data)

def method(request):


        gradelen = Category.objects.count()         #
        #sups2 = list(Category.objects.all())
        catlen = Grades.objects.count()             #

        grades = Grades.objects.all()
        mass = []
        for p in grades:
            buf = list(json.loads(p.chargrade))
            buf2 = buf.copy()
            mass.append(buf2)

        markmass = []
        for j in range(gradelen):
            mark = 0
            for i in range(catlen):
                mark = mark + mass[i][j]
            markmass.append(mark)
        sum = 0
        for i in markmass:
            sum = sum + i

        leng = len(markmass)
        for i in range(leng):
            markmass[i]= markmass[i]/sum


        cats = list(Category.objects.all())
        for i in range(gradelen-1):
            for j in range(gradelen-i-1):
                if markmass[j] < markmass[j+1]:
                    markmass[j], markmass[j+1] = markmass[j+1], markmass[j]
                    bbuf =cats[j]
                    cats[j] = cats[j+1]
                    cats[j+1] = bbuf



        data = {'cats':cats, 'mass':markmass}
        return render(request, "mass.html", context=data)
