from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Poll,Choice
from . import forms
from django.forms import modelformset_factory
from django.db.models import Q

def home(request):

    sortform = forms.SortForm(request.GET or None)
    sort_option = request.GET.get('sort_by')

    qs = None
    if sort_option == 'new' or sort_option == None:
        qs = Poll.objects.order_by('-date_posted')
    if sort_option == 'old':
        qs = Poll.objects.order_by('date_posted')
    elif sort_option == 'top':
        qs = Poll.objects.order_by('-total_votes')
    

    context = {
        'polls' : qs,
        'title' : 'Poller - Home',
        'sortform': sortform
    }

    return render(request,'polls/home.html',context)
    

def detail(request, poll_id):
    poll = get_object_or_404(Poll,pk=poll_id)

    if request.user in poll.users_voted.all():
        return HttpResponseRedirect(reverse('polls:results',args=[poll_id]))
    else:

        VotingForm = forms.createVotingForm(poll_id=poll_id)
        
        if request.method == 'POST':

            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('login')+f"?next={request.path}")
                
            form = VotingForm(request.POST)
            
            if form.is_valid():
                selected_choices_id = form.cleaned_data.get('multiple_choice_field')
                selected_choices = []
                for choice_id in selected_choices_id:
                    selected_choices.append(poll.choice_set.get(id=choice_id))
                
                for selected_choice in selected_choices:
                    selected_choice.vote_count += 1
                    selected_choice.voted_by.add(request.user)
                    poll.total_votes +=1
                    selected_choice.save()

                poll.users_voted.add(request.user)
                poll.save()
            
                return redirect('polls:results',poll_id=poll_id)

        else:
            form = VotingForm()

        return render(request,'polls/detail.html',{'form':form,'choices':form.fields['multiple_choice_field'].choices , 'poll':poll ,'title':f"Poll no: {poll_id}"})
    


def results(request, poll_id):

    poll = get_object_or_404(Poll,pk=poll_id)
    perc_choice_pairs = [(round((choice.vote_count / poll.total_votes) * 100),choice) for choice in poll.choice_set.all()]

    if request.user in poll.users_voted.all():
        if poll.public_results == True:
            context = {
                'poll':poll,
                'pairs':perc_choice_pairs,
            }
        else:
            if request.user == poll.author:
                context = {
                'poll':poll,
                'pairs':perc_choice_pairs,
            }
            else:
                context = {
                    'poll': None,
                }

        return render(request,'polls/results.html',context)
    else:
        return redirect('polls:detail',poll_id=poll_id)

def create(request):
    ChoiceFormSet = modelformset_factory(Choice,fields=('choice_text',),extra=0,min_num=2,formset=forms.ChoiceFormSet,validate_min=True)
    qs = Choice.objects.none()

    if request.method == 'POST':

        choiceformset = ChoiceFormSet(request.POST)
        pollform = forms.PollForm(request.POST)

        if choiceformset.is_valid() and pollform.is_valid():
            parentpoll = pollform.save(commit=False)
            parentpoll.author = request.user
            parentpoll.save()

            choices = choiceformset.save(commit=False)

            for choice in choices:
                choice.parent_poll = parentpoll
                choice.save()
                
            messages.success(request,'Poll created successfully')
            return redirect(reverse('polls:detail',args=[parentpoll.id]))
        
    else:
        choiceformset = ChoiceFormSet(queryset=qs)
        pollform = forms.PollForm()

    context = {
        'choiceformset':choiceformset,
        'pollform':pollform,
    }
    
    for error in choiceformset.non_form_errors():
        print(error)

    return render(request,'polls/create.html',context)

def search(request):

    search = request.GET.get('search')
    sort = request.GET.get('sort_by')
    anon = request.GET.get('anonymity')
    results = request.GET.get('results_access')

    qs = Poll.objects.all()

    if anon == 'anon':
        qs = Poll.objects.filter(anonymous_poll=True)
    elif anon == 'nonon':
        qs = Poll.objects.filter(anonymous_poll=False)

    if results == 'public':
        qs = qs.filter(public_results=True)
    elif results == 'private':
        qs = qs.filter(public_results=False)

    qs = qs.filter(Q(description__contains=search) | Q(title__contains=search))

    if sort == 'new':
        qs = qs.order_by('-date_posted')
    elif sort == 'old':
        qs = qs.order_by('date_posted')
    elif sort == 'top':
        qs = qs.order_by('-total_votes')

    context = {
        'polls':qs
    }

    print(qs)

    return render(request,'polls/search.html',context)