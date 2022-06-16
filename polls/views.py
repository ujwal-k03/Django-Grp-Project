from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, Http404
from .models import Poll

def about(request):
    return HttpResponse('You are at polls about')

def home(request):
    context = {
        'polls' : Poll.objects.order_by('-date_posted'),
    }
    return render(request,'polls/home.html',context)
    

def detail(request, poll_id):
    poll = get_object_or_404(Poll,pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
    return HttpResponse("You're looking at the results of question %s." % poll_id)

def vote(request, poll_id):
    return HttpResponse("You're voting on question %s." % poll_id)