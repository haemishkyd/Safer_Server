from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question
from django.contrib.auth.models import User
from appinterface.models import Operator

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    user_details = User.objects.all()

    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
        'user_details':user_details,
    }
    return HttpResponse(template.render(context, request))
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])
    # operators_list = User.objects.all()
    # output_name = ', '.join([o.operator.company for o in operators_list])
    
    # return HttpResponse("Hello, world. You're at the polls index."+output+output_name)

