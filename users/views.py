from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from polls.forms import SortForm
from polls.models import Poll

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            new_user = authenticate(username = form.cleaned_data['username'],password=form.cleaned_data['password1'],)
            login(request,new_user)
            messages.success(request,f'Account Created for {username}!')
            return redirect('polls:home')
    else:
        form = UserRegisterForm()

    return render(request,'users/register.html',{'form':form})


def profile(request,user_id):
    
    requested_user = get_object_or_404(User,id=user_id)

    sortform = SortForm(request.GET or None)
    sort_option = request.GET.get('sort_by')

    qs = None
    if sort_option == 'new' or sort_option == None:
        qs = requested_user.poll_set.order_by('-date_posted')
    if sort_option == 'old':
        qs = requested_user.poll_set.order_by('date_posted')
    elif sort_option == 'top':
        qs = requested_user.poll_set.order_by('-total_votes')

    if request.user == requested_user and request.user.is_authenticated:
        if request.method == 'POST':
            uform = UserUpdateForm(request.POST,instance=request.user)
            pform = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

            if uform.is_valid() and pform.is_valid():
                uform.save()
                pform.save()
                messages.success(request,f'Account updates successfully!')
                return redirect('profile',user_id = request.user.id)
        else:
            uform = UserUpdateForm(instance=request.user)
            pform = ProfileUpdateForm(instance=request.user)

        context = {
            'u_form':uform,
            'p_form':pform,
            'user':requested_user,
            'allow_edit':True,
            'polls':qs,
            'sortform':sortform,
        }
    else:

        context = {'user':requested_user,'allow_edit':False,'polls':qs,'sortform':sortform,}


    return render(request,'users/profile.html',context)

