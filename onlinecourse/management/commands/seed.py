from django.core.management.base import BaseCommand

import os
import sys
import django

from django.contrib.auth.models import User
from onlinecourse.models import Instructor, Learner, Course, Lesson, Enrollment, Question, Choice, Exam

class Command(BaseCommand):
    help = 'Seeds the database with initial data.'

    def handle(self, *args, **options):
        # Add your seed logic here
        
        # Create Users
        user1 = User.objects.create_user('john.doe', 'john.doe@example.com', 'password')
        user2 = User.objects.create_user('jane.smith', 'jane.smith@example.com', 'password')

        # Create Instructors
        instructor1 = Instructor.objects.create(user=user1, full_time=True, total_learners=10)
        instructor2 = Instructor.objects.create(user=user2, full_time=False, total_learners=5)

        # Create Learners
        learner1 = Learner.objects.create(user=user1, occupation=Learner.STUDENT, social_link='https://example.com/john.doe')
        learner2 = Learner.objects.create(user=user2, occupation=Learner.DATA_SCIENTIST, social_link='https://example.com/jane.smith')

        # Create Courses
        course1 = Course.objects.create(name='Physics Course', description='Introduction to Physics', pub_date='2023-06-30', total_enrollment=20)
        course2 = Course.objects.create(name='Math Course', description='Advanced Mathematics', pub_date='2023-07-01', total_enrollment=15)

        # Add Instructors to Courses
        course1.instructors.add(instructor1)
        course2.instructors.add(instructor2)

        # Add Users (Learners) to Courses through Enrollment
        enrollment1 = Enrollment.objects.create(user=user1, course=course1, mode=Enrollment.HONOR)
        enrollment2 = Enrollment.objects.create(user=user2, course=course2, mode=Enrollment.AUDIT)

        # Create Lessons
        lesson1 = Lesson.objects.create(title='Introduction to Mechanics', order=1, course=course1, content='Lesson content goes here.')
        lesson2 = Lesson.objects.create(title='Calculus Fundamentals', order=2, course=course1, content='Lesson content goes here.')
        lesson3 = Lesson.objects.create(title='Linear Algebra', order=1, course=course2, content='Lesson content goes here.')
        lesson4 = Lesson.objects.create(title='Probability Theory', order=2, course=course2, content='Lesson content goes here.')

        # Create Questions
        question1 = Question.objects.create(lesson=lesson1, question='What is Newton\'s first law of motion?', grade=5.0)
        question2 = Question.objects.create(lesson=lesson2, question='What is the derivative of x^2?', grade=5.0)
        question3 = Question.objects.create(lesson=lesson3, question='What is a matrix determinant?', grade=5.0)
        question4 = Question.objects.create(lesson=lesson4, question='What is the probability of rolling a dice and getting a 3?', grade=5.0)

        # Create Choices for Questions
        choice1 = Choice.objects.create(content='An object at rest stays at rest', is_correct=True)
        choice2 = Choice.objects.create(content='An object in motion stays in motion', is_correct=False)
        choice3 = Choice.objects.create(content='3x', is_correct=True)
        choice4 = Choice.objects.create(content='2x', is_correct=False)
        choice5 = Choice.objects.create(content='A property of matrices', is_correct=True)
        choice6 = Choice.objects.create(content='A property of vectors', is_correct=False)

        question1.choice.add(choice1, choice2)
        question2.choice.add(choice3, choice4)
        question3.choice.add(choice5, choice6)
        question4.choice.add(choice1, choice2)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
