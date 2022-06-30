from django.shortcuts import get_object_or_404
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Poll

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['title','description','no_of_options_to_be_selected','anonymous_poll','public_results']

class ChoiceFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(ChoiceFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

class SortForm(forms.Form):
    choices_tuple = [
        ('new','New'),
        ('old','Old'),
        ('top','Top'),
    ]

    sort_by = forms.ChoiceField(widget=forms.Select,choices=choices_tuple)

class SearchForm(forms.Form):
    
    anon_tuple = [
        ('any','Any'),
        ('anon','Anonymous'),
        ('nonon','Non-Anonymous'),
    ]
    results_tuple = [
        ('any','Any'),
        ('public','Public'),
        ('private','Private'),
    ]
    order_tuple = [
        ('new','New'),
        ('old','Old'),
        ('top','Top'),
    ]

    search = forms.CharField(required=False)
    search_sort_by = forms.ChoiceField(widget=forms.Select,choices=order_tuple)
    anonymity = forms.ChoiceField(widget=forms.Select,choices=anon_tuple)
    results_access = forms.ChoiceField(widget=forms.Select,choices=results_tuple)
        
def createVotingForm(poll_id):
    poll = get_object_or_404(Poll,pk=poll_id)
    choices_tuple = [(c.id,c.choice_text) for c in poll.choice_set.all()]

    class VotingForm(forms.Form):
        multiple_choice_field = forms.MultipleChoiceField(choices=choices_tuple,widget=forms.CheckboxSelectMultiple(attrs={'class':'check'}))

        def clean(self):
            
            cleaned_data = super().clean()

            if(cleaned_data.get('multiple_choice_field')):
                if len(cleaned_data.get('multiple_choice_field')) != poll.no_of_options_to_be_selected:
                    raise ValidationError(f"You have to choose exactly {poll.no_of_options_to_be_selected} options")

    return VotingForm

