import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

from django.contrib.auth.models import User
from models import Instructor, Learner, Course, Lesson, Enrollment, Choice, Exam, Question

def seed_data():
    # Create users
    instructor_user = User.objects.create_user(username='instructor', password='password')
    learner_user = User.objects.create_user(username='learner', password='password')

    # Create instructors
    instructor = Instructor.objects.create(user=instructor_user, full_time=True, total_learners=100)

    # Create learners
    learner = Learner.objects.create(user=learner_user, occupation=Learner.STUDENT, social_link='https://example.com')

    # Create a course
    course = Course.objects.create(name='Web Development', description='Learn web development', pub_date='2023-05-12')

    # Add instructors to the course
    course.instructors.add(instructor)

    # Add learners to the course through enrollment
    enrollment = Enrollment.objects.create(user=learner_user, course=course)

    # Create lessons
    lesson1 = Lesson.objects.create(title='Lesson 1', order=1, course=course, content='Lesson 1 content')
    lesson2 = Lesson.objects.create(title='Lesson 2', order=2, course=course, content='Lesson 2 content')

    # Create choices
    choice1 = Choice.objects.create(content='Choice 1', is_correct=True)
    choice2 = Choice.objects.create(content='Choice 2', is_correct=False)
    choice3 = Choice.objects.create(content='Choice 3', is_correct=False)

    # Create questions
    question1 = Question.objects.create(lesson=lesson1, question='Question 1', grade=5.0)
    question1.choices.add(choice1, choice2)

    question2 = Question.objects.create(lesson=lesson2, question='Question 2', grade=4.0)
    question2.choices.add(choice1, choice3)

    # Print the created objects
    print("Instructor:", instructor)
    print("Learner:", learner)
    print("Course:", course)
    print("Enrollment:", enrollment)
    print("Lesson 1:", lesson1)
    print("Lesson 2:", lesson2)
    print("Question 1:", question1)
    print("Question 2:", question2)


# Call the seed_data() function to populate the database
seed_data()