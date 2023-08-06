from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Contact
from blog.models import Post
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate



# Create your views here.
def home(request):
    allpost=Post.objects.all()
    paginator = Paginator(allpost, 3)  # Paginate the items with 3 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_pages = paginator.num_pages
    return render(request,'home/home.html',{'allpost':allpost,'page_obj':page_obj,'total_pages':total_pages,})
def about(request):
    return render(request,'home/about.html')
def blog(request):
    allpost=Post.objects.all()
    paginator = Paginator(allpost, 1)  # Paginate the items with 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_pages = paginator.num_pages
    return render(request, 'home/blog.html',{'page_obj':page_obj,'total_pages':total_pages,'allpost':allpost})

def blogPost(request, slug):
    post=Post.objects.filter(slug=slug).first()
    return render(request, 'home/blogpost.html',{'post':post})
   
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        content=request.POST.get('content')
        contactdata=Contact(name=name,email=email,phone=phone,content=content),
        if len(name)<2 or len(email)<10 or len(phone)<3 or len(content)<10:
            messages.error(request, 'Please fill the form correctly')
            
        else:
            contactdata.save()
           
            messages.success(request, 'your Message has been sent')
       

    return render(request,'home/contact.html')


def Search(request):
    # query=request.GET['query']
    # if query==

    # data1=Post.objects.filter(title__icontains=query)
    # data2=Post.objects.filter(content__icontains=query)
    # searched_data=data1.union(data2)
    # return render(request,'home/search.html',{'result':searched_data})
    query=request.GET['query']
    if len(query)>78:
        allpost=Post.objects.none()
    else:
        allpostTitle=Post.objects.filter(title__icontains=query)
        allpostContent=Post.objects.filter(content__icontains=query)
        allpost=allpostTitle.union(allpostContent)
    if allpost.count()==0:
        messages.warning(request,"No search result found. Please refine your query")
    params={'allpost':allpost, 'query':query}
    return render(request, 'home/search.html',params)

# def item_list(request):
#     items = Post.objects.all()
#     paginator = Paginator(items, 1)  # Paginate the items with 10 items per page
    
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     context = {
#         'page_obj': page_obj
#     }
    
#     return render(request, 'home/blog.html', context)



def HandleSignup(request):
    if request.method=="POST":
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if len(fname)<=2 or len(lname)<=1:
            messages.error(request,'fname and lname must be greater than 2')
            return redirect('home')
        if pass1!=pass2:
            messages.error(request,'password do not match ')
            return redirect('home')
        if len(username)>=10:
            messages.error(request,'Username must be under 10 character')
            return redirect('home')
        if username.isalnum():
             messages.error(request, ' username must contain alphabet and number')
             return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request,"email already Exists")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username  already Exists")
            return redirect('home')
        user=User.objects.create_user(username,email,pass1)
        user.first_name=fname
        user.last_name=lname
        user.save()
        messages.success(request,'Your account has been created Successfully')
        return redirect('home')
    

def HandleLogin(request):
    if request.method=="POST":
        loginusername=request.POST.get('loginusername')
        loginpassword=request.POST.get('loginpassword')
        user=authenticate(request,username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,"You are Successfull logged in ")
            return redirect('home')
        else:
            messages.error(request,"user does not exits")
            return redirect('home')
    else:
        return HttpResponse("user does not exits")


def HandleLogout(request):
    logout(request)
    messages.success(request,"You are sucessfullu Logged Out")
    return redirect('home')
        