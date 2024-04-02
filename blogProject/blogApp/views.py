from django.shortcuts import render, redirect,get_object_or_404
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
# from django.contrib.auth.models import User   # using this line gives this error sol is below "Manager isn't available; 'auth.User' has been swapped for 'blogApp.CustomUser'"
from django.contrib.auth import get_user_model
User = get_user_model()
from blogApp.models import CustomUser, Category, Blog, Like, Rating
from django.http import JsonResponse


def home_view(request):

    next_url = request.session.pop('next', '/')
    categories = Category.objects.all()
    # print(categories)
    blogs = Blog.objects.filter(status = True)
    
    context = {'blogs' : blogs, 'categories' : categories}
    return render(request,'blogs.html',context )

def login_view( request):
    # print(request.user)
    # print(request.user.id)
    next_url = request.POST.get('next') or request.GET.get('next')
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        
        user = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = user, password = password)
        if user:
            login(request, user)
            
            
            return redirect(next_url or 'home')  # i missed this one and result of it will render on same page again nd again
        context = {}

        if user is None:
            context = {'error': "Invalid username or password"}
            return render(request, 'login.html', context)
        return redirect(next_url or 'home')
    
    return render(request,'login.html')

def profile_view(request, req_user_id):
    if request.user.is_authenticated:
        requested_data_user = CustomUser.objects.get(id = req_user_id)
        current_user = request.user

        followers = requested_data_user.followers.all()
        num_following = requested_data_user.following.count()
        is_admin = current_user.is_admin_user()
        # print(is_admin)
        myBlogs = Blog.objects.filter(author=requested_data_user, status = True)
        is_followed = requested_data_user.followers.filter(id=request.user.id).exists()
        # print(is_followed)
        # print(myBlogs)
        # print( user.is_admin_user())
        # print(followers.count())
        context = {'followers_count' : followers.count(), 'following_count' : num_following, 'is_admin' : is_admin, 'myBlogs': myBlogs, 'requested_user': requested_data_user, 'req_user_id' :req_user_id, 'is_followed':is_followed }
        return render(request, 'profile.html', context)
    
    return redirect('login')

def follow_user(request, req_user_id):
    print(request.method)
    if request.user.is_authenticated:
        if( request.user.id == req_user_id):
            return redirect('profile', req_user_id = request.user.id)
        user_to_follow = CustomUser.objects.get(id = req_user_id)
        print(user_to_follow)
        user_to_follow.followers.add(request.user)
        # request.user.following.add( user_to_follow) # as we can use this method also
        return redirect('profile', req_user_id= req_user_id)

    return redirect('login')    

def logout_view( request):
    if request.user.is_authenticated:
        logout(request)
        # return render(request,'login.html')  # this will only render login.html code while url will be same of logout 
        return redirect('login')
    return redirect('login')


def user_signup(request):
    if request.method == 'POST':
        # Get data from the request
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Validate password and confirm_password
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        # Create a new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        redirect('home')
    return render(request, 'signup.html')  # Adjust the template name as needed


def category_view(request, category_id):
    category = Category.objects.get(id = category_id)
    # print(category)
    blogs = Blog.objects.filter(categories = category, status = True)
    # print(blogs)
    context = {"blogs": blogs, 'category':category}

    return render (request, 'category.html', context)

def update_blog( request, blog_id):

    if request.user.is_authenticated:

        blog = Blog.objects.get(id = blog_id)
        if request.method == 'POST':
            
            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            # print(data)
            blog.title = data.get('title')
            blog.content = data.get('content')
            blog.image_field = data.get('image')
            
            # print(image_field)
            categories = data.get('categories')
            # print(categories)
            try:
                blog.categories.clear()
                for category_id in categories:
                    category = Category.objects.get(id=category_id)
                    blog.categories.add(category)
                blog.save()
                return JsonResponse({'message': 'Blog updated successfully', 'id':request.user.id}, status=201)
            except Exception as e:
                print("e",e)
                
                return JsonResponse({'error': str(e)}, status=500)
        return render(request, 'update_blog.html', {'blog_id': blog_id})
    return redirect('login')

def delete_blog(request, blog_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(blog_id)
            print("delete")
            blog = get_object_or_404(Blog, id=blog_id)
            blog.delete()
            return JsonResponse({'message': 'Blog deleted successfully'})
        return JsonResponse({'message': 'invalid request'})
    return JsonResponse({'message': 'you must be login', 'nextUrl': request.path})

def like_blog(request, blog_id):
    print(request.method)
    next = request.path
    if request.user.is_authenticated:
        if request.method == "POST":
            blog = Blog.objects.get(id = blog_id)
            user = request.user
            message = 'error'
            if not Like.objects.filter(user=user, blog=blog).exists():
                Like.objects.create(user=request.user, blog=blog)
                message = 'blog liked by the user successfully'
            else:
                message = 'user already liked this post'
            return JsonResponse({'message': message})   
        return JsonResponse({'message': 'invalid request'})
    return JsonResponse({'message': 'you must be login', 'nextUrl': next})


def show_drafts(request):
    if request.user.is_authenticated:
        if request.user.is_admin_user():
            pending_blogs = Blog.objects.filter(status = False)
            # print(pending_blogs)
            return render(request, 'drafts.html', {'pending_blogs': pending_blogs})
        return redirect('admin:index')  
    return redirect('login')
    
def publish_blog(request, blog_id):
    if request.user.is_authenticated:
        if request.user.is_admin_user:
            blog = Blog.objects.get(id = blog_id)
            blog.status = True
            blog.save()
            return JsonResponse({'message': 'Blog published successfully'})
        return redirect('admin:index')  
    return redirect('login')

def createBlog_view( request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # print(request.POST.dict())
            author = request.user
            # Load JSON data from the request body
            data = json.loads(request.body.decode('utf-8'))
            # print(data)
            title = data.get('title')
            content = data.get('content')
            image_field = data.get('image')
            
            # print(image_field)
            categories = data.get('categories')
            # print(categories)
            try:
                blog = Blog.objects.create(title = title, content = content , author = author, image_field = image_field)
                for category_id in categories:
                    category = Category.objects.get(id=category_id)
                    blog.categories.add(category)
                blog.save()
                return JsonResponse({'message': 'Blog created successfully', 'id':request.user.id}, status=201)
            except Exception as e:
                print("e",e)
                
                return JsonResponse({'error': str(e)}, status=500)
                

            return redirect('home')
        else:
            print(request)
            return render( request, 'createBlog.html')


    return redirect('login')    

def rateBlog(request, blog_id):
    if request.user.is_authenticated:
        print('rate')
        blog = Blog.objects.get(id = blog_id)
        value = request.POST.get('rating')
        print(value)
        Rating.objects.create(blog = blog, user = request.user, value = value)
        JsonResponse({'message': 'rating has been done successfully'})
    
    return JsonResponse({'message': 'you must be login'})


def blog_view(request, blog_id):
    if request.user.is_authenticated:
        return render(request, 'blogView.html')
    

