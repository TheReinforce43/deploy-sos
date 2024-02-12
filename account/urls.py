from django.urls import path
from account.views import UserRegistration, UserLogin,TeacherApproveView, TeacherListCreateView, TeacherRetrieveUpdateDestroyView
from account.views import CategoryListCreateView,CategoryRetrieveUpdateDestroyView
from account.views import TeacherUserListView,StudentUserListView,AdminListView
from account.views import CourseListCreateView,CourseRetrieveUpdateDestroyView
from account.views import SingleStudent,SingleTeacher,TeacherWiseCourses
from account.views import EnrollmentModelView
urlpatterns = [   
    path('register/', UserRegistration.as_view(), name='user_registration'),
    path('login/', UserLogin.as_view(), name='user_login'),

    # get all teacher users
    path('approved-teachers/', TeacherUserListView.as_view(), name='all-teachers'),
    # get all students users
    path('students/', StudentUserListView.as_view(), name='all-teachers'),
    path('admins/', AdminListView.as_view(), name='all-admins'),


     # Teacher urlw
    path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherRetrieveUpdateDestroyView.as_view(), name='teacher-retrieve-update-destroy'),

    # teacher Approved view 
    path('approve-teacher/<int:pk>/',TeacherApproveView.as_view(),name="teacher-approve-view"),

    # retrieve single student
    path('student/<int:pk>/',SingleStudent.as_view(),name="single-student"),

    # retrieve single teacher
    path('teacher/<int:pk>/',SingleTeacher.as_view(),name="single-teacher"),




    # course category
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),

    # course urls
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course-retrieve-update-destroy'),

    #teacher wise courses
    path('teacher/<int:teacher_id>/courses/', TeacherWiseCourses.as_view(), name='teacher-courses'),

    # Enrollment
    path('sold-courses/', EnrollmentModelView.as_view(), name='all-sold-courses'),
    path('student-courses/<int:student_id>/', EnrollmentModelView.as_view(), name='student-bought-courses'),
    path('enroll-course/', EnrollmentModelView.as_view(), name='enroll-course'),
    
]