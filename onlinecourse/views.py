from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Course, Exam, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


@login_required
@require_POST
def submit(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    submission = Submission.objects.create(exam=exam, user=request.user, score=0)
    total = 0
    score = 0

    for question in exam.questions.all():
        total += question.grade
        selected_ids = request.POST.getlist(f"question_{question.id}")
        selected_choices = Choice.objects.filter(question=question, id__in=selected_ids)
        submission.choices.add(*selected_choices)
        if question.is_get_score(selected_ids):
            score += question.grade

    submission.score = score
    submission.save()
    request.session[f"submission_{submission.id}_total"] = total
    return redirect("show_exam_result", submission_id=submission.id)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, user=request.user)
    total = request.session.get(f"submission_{submission.id}_total")
    if total is None:
        total = sum(q.grade for q in submission.exam.questions.all())
    questions = submission.exam.questions.prefetch_related("choice_set").all()
    passed = bool(total) and submission.score >= total
    return render(
        request,
        "onlinecourse/exam_result.html",
        {"submission": submission, "total": total, "questions": questions, "passed": passed},
    )


@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = exam.questions.prefetch_related("choice_set").all()
    return render(request, "onlinecourse/take_exam.html", {"exam": exam, "questions": questions})
