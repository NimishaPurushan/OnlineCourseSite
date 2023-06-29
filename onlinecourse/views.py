from django.shortcuts import render
from django.http import HttpResponseRedirect
# <HINT> Import any new Models here
from .models import Course, Enrollment, Submission, Choice, Question, Exam
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import login, logout, authenticate
import logging
# Get an instance of a logger


logger = logging.getLogger(__name__)
# Create your views here.


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'onlinecourse/user_registration_bootstrap.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("onlinecourse:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'onlinecourse/user_registration_bootstrap.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'onlinecourse/user_login_bootstrap.html', context)
    else:
        return render(request, 'onlinecourse/user_login_bootstrap.html', context)


def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')


def check_if_enrolled(user, course):
    is_enrolled = False
    if user.id is not None:
        # Check if user enrolled
        num_results = Enrollment.objects.filter(user=user, course=course).count()
        if num_results > 0:
            is_enrolled = True
    return is_enrolled


# CourseListView
class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'

    def get_queryset(self):
        user = self.request.user
        courses = Course.objects.order_by('-total_enrollment')[:10]
        for course in courses:
            if user.is_authenticated:
                course.is_enrolled = check_if_enrolled(user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user

    is_enrolled = check_if_enrolled(user, course)

    questions = Question.objects.filter(lesson__course=course)
    
    print(user)
    print(course)
    print(questions)
    for q in questions:
        print(q.choice)
    context = {
        'course': course,
        'questions': questions
    }

    if not is_enrolled and user.is_authenticated:
        # Create an enrollment
        Enrollment.objects.create(user=user, course=course, mode='honor')
        course.total_enrollment += 1
        course.save()
    return render(request, 'onlinecourse/course_detail_bootstrap.html', context)
    #return HttpResponseRedirect(reverse(viewname='onlinecourse:course_details', args=(course.id, questions)))


# <HINT> Create a submit view to create an exam submission record for a course enrollment,
# you may implement it based on following logic:
         # Get user and course object, then get the associated enrollment object created when the user enrolled the course
         # Create a submission object referring to the enrollment
         # Collect the selected choices from exam form
         # Add each selected choice object to the submission object
         # Redirect to show_exam_result with the submission id
def submit(request, course_id):
    user = request.user
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=user, course=course)

    

    if request.method == 'POST':
        submission = Submission.objects.create(enrollment=enrollment)
        selected_choices = request.POST.getlist('choices')
        logger.info(f"From Submit, choice is {selected_choices}")

        selected_choices = []
        for key in request.POST:
            if key.startswith('choice_'):
                choice_id = key.split('_')[1]  # Extract the choice ID from the key
                selected_choices.append(choice_id)
        logger.info(f"From Submit choice, choice is {selected_choices}")
        for choice_id in selected_choices:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)

        submission_id = submission.id
        redirect_url = reverse('onlinecourse:show_exam_result', kwargs={'course_id': course_id, 'submission_id': submission_id})
        return redirect(redirect_url)

    context = {
        'user': user,
        'course': course
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)


# <HINT> A example method to collect the selected choices from the exam form from the request object
def extract_answers(request):
   submitted_anwsers = []
   for key in request.POST:
       if key.startswith('choice'):
           value = request.POST[key]
           choice_id = int(value)
           submitted_anwsers.append(choice_id)
   return submitted_anwsers


# <HINT> Create an exam result view to check if learner passed exam and show their question results and result for each question,
# you may implement it based on the following logic:
        # Get course and submission based on their ids
        # Get the selected choice ids from the submission record
        # For each selected choice, check if it is a correct answer or not
        # Calculate the total score
#def show_exam_result(request, course_id, submission_id):
def show_exam_result(request, course_id, submission_id):
    # Get course and submission based on their ids
    course = get_object_or_404(Course, id=course_id)
    submission = get_object_or_404(Submission, id=submission_id)

    # Get the selected choice ids from the submission record
    selected_choice_ids = submission.choices.values_list('id', flat=True)
    logger.info(f"Selected ids from outer choice is {selected_choice_ids}")
    # Initialize variables for score calculation
    total_score = 0
    question_results = []
    expected_score = 0
    # For each question, check if the selected choices are correct or not
    for question in Question.objects.filter(lesson__course=course):
        is_correct = question.is_get_score(selected_choice_ids)
        if is_correct:
            total_score += question.grade
        expected_score += question.grade
        logger.info("Total Score: %s, Is Correct: %s", total_score, is_correct)
        question_results.append({
            'question': question.question,
            'choices': question.choice.all(),
            'is_correct': is_correct
        })

    # Render the exam result template with the calculated data
    context = {
        'course': course,
        'submission': submission,
        'question_results': question_results,
        'total_score': total_score*100/ expected_score,
        "selected_choice_ids" : selected_choice_ids
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)

