from multiprocessing import AuthenticationError
import re
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout,authenticate
from .forms import  ProfileForm,  Profile
from .models import Team
from django.db.models.query_utils import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    context={}
    if request.user.is_authenticated:
        teammates = Profile.objects.filter(Q(team=request.user.team)&~Q(id=request.user.id))
        print(teammates)
        context['team']=teammates
    return render(request, 'home.html', context)
def login(request):
    if request.method == 'POST':
        form = AuthenticationError(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect('home')
            else:
                #messages.error(request,'User blocked',extra_tags='login')
                return redirect('login')
        else:
            #messages.error(request,'username or password not correct',extra_tags='login')
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html',{'form':form})
@login_required(login_url='/login')
def add(request):
    context={}
    add_form = ProfileForm(request.POST or None)
    context['addForm']=add_form
    try:
        user = Profile.objects.get(id=request.user.id)
        print(user)
    except Exception as e:
        print(str(e))
        return redirect('home')
    
    if request.method=="POST":
        #for f in request.user._meta.fields:
            #print(f.name, getattr(request.user, f.name))
        
        if request.user.team is None:     
            new_team = Team()
            new_team.save()
            user.team=new_team
            user.save()
            print(Team.objects.all().first().id)
            print(user.team)

        if add_form.is_valid():
            #add_form.password=new_password
            #add_form.save() 
            post = request.POST
            print(post['email'])
            new_password = post['first_name']+post['last_name']
            print(new_password)

            new_user = Profile.objects.create_user(
                email = post['email'],
                password=new_password,
                team=user.team,
                first_name=post['first_name'],
                last_name=post['last_name'],
                phone_number=post['phone_number'],
                is_edit=post['is_edit']
            )
            new_user.save()
            
            return redirect('home')
        else:
            return render(request, 'add.html',context)
        
    else:
        pass
    return render(request, 'add.html',context)
@login_required(login_url='/login')
def edit(request,user_id):
    context={}
    try:
        user = Profile.objects.get(id=user_id)
        print(user,user_id)
    except Exception as e:
        print(str(e))
        return redirect('home')
    print(user.team,request.user.team)
    context['team']=user.team
    context['is_edit']=request.user.is_edit
    #Currently logged in user has to have is_edit? and be the same team
    if request.user.team != user.team or request.user.is_edit==False:
        return redirect('home')
    
    if request.method=="POST":
        if "editProfileForm" in request.POST:
            print('Editing')
            edit_profile_form = ProfileForm(request.POST or None,instance=user)
            if edit_profile_form.is_valid(): 
                edit_profile_form.save()
                print(edit_profile_form)
                return redirect('home')
            else:
                context['editProfileForm'] = edit_profile_form
                return render(request,'edit.html',context)
        if "deleteProfileForm" in request.POST:
            print('Deleting')
            try:
                user.delete()
                #messages.success(request, "The user is deleted")            

            except Exception as e:
                #messages.error(request, "User does not exist")   
                print(str(e)) 
                pass

            return redirect('home')
       
    else:
        edit_profile_form = ProfileForm(request.POST or None,instance=user)
        context['editProfileForm'] = edit_profile_form
    return render(request,'edit.html',context)