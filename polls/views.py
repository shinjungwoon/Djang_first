#함수연결
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Question, Choice
from django.http import Http404

from django.db.models import F
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone

# def index(request):
#     # return HttpResponse("Hello, world. You're at the polls index.")
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

# # def detail(request, question_id):
# #     question = get_object_or_404(Question, pk=question_id)
# #     return render(request, "polls/detail.html", {"question": question})

# def results(request, question_id):
#     # question = get_object_or_404(Question, pk=question_id)
#     # return render(request, "polls/results.html", {"question": question})
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})
# def vote(request, question_id):
#     return HttpResponse(f"You're voting on question {question_id}.")

class IndexView(generic.ListView):
  template_name = "polls/index.html"
  context_object_name = "latest_question_list"

  def get_queryset(self):
      return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
  model = Question
  template_name = "polls/detail.html"
  context_object_name = "question"

  def get_queryset(self):
      return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
  model = Question
  template_name = "polls/results.html"
  context_object_name = "question"

  def get_queryset(self):
      return Question.objects.filter(pub_date__lte=timezone.now())

# 투표 처리 로직
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message":"You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse
        ("polls:results", args=(question.id,)))
    

# CRUD
# 생성하기(글쓰기)
class QuestionCreateView(generic.CreateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")

#읽기(상세보기, 수정하기)
class QuestionUpdateView(generic.UpdateView):
  model = Question
  fields = ["question_text", "pub_date"]
  template_name = "polls/question_form.html"
  success_url = reverse_lazy("polls:index")
  
#삭제하기
class QuestionDeleteView(generic.DeleteView):
  model = Question
  template_name = "polls/question_form_delete.html"
  success_url = reverse_lazy("polls:index")
    