from django.shortcuts import get_object_or_404, render

# Create your views here.

from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.urls import reverse
from .models import Choice, Question


def index(request):
    latest_q_list = Question.objects.order_by('-pub_date')[:5]
    context = {
          'latest_q_list': latest_q_list,
    }
    return render(request, 'polls/index.html', context) #HttpResponse(template.render(context, request))

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

   # can also use 
   # quesion = get_object_or_404(Question, pk=question_id)
   # as a shortcut in place of the entire try except

    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You are looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 
                       'polls/detail.html', {'question': question,
                       'error_message': "You didn't select a choice.",
                       })
    else:
        selected_choice.votes += 1
        selected_choice.save()

	              
    return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))
