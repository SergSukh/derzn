from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from drevo.models import QuizResult


@login_required
def show_quiz_result(request):
    if request.method == 'GET':
        quiz_results = {}
        all_results = QuizResult.objects.filter(user=request.user)
        all_quizzes_name = all_results.values_list("quiz__name", flat=True).distinct()
        for quizzes in all_quizzes_name:
            questions_and_answers = {}
            all_questions_name = all_results.filter(quiz__name=quizzes).values_list("question__name", flat=True) \
                .distinct().order_by('-question__order')
            for questions in all_questions_name:
                questions_and_answers[questions] = all_results.filter(question__name=questions, quiz__name=quizzes) \
                    .values_list("answer__name", "answer__related__tr__name").order_by('-answer__order')
            date = str(all_results.filter(quiz__name=quizzes).values_list("date_time__day", "date_time__month",
                                                                          "date_time__year").first()).rstrip(')'). \
                lstrip('(').replace(' ', '')
            for_link = all_results.filter(quiz__name=quizzes).values_list("quiz__pk", flat=True).first()
            quiz_results[quizzes + ' ' + date.replace(',', '.') + ' ' + str(for_link)] = questions_and_answers
        return render(request, 'drevo/show_quiz_result.html', {'quiz_result': quiz_results})