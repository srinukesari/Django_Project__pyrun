from django.urls import path
from . import views

urlpatterns = [
    path('home_quote',views.home_quote),
    path('signup',views.signup),
    path('login',views.login),
    path('logout',views.logout),
    path('loader',views.loader),
    path('user_practise',views.user_practise),
    path('user_challenges',views.user_challenges),
    path('user_solve',views.user_solve),
    path('user_execute',views.user_execute),
    path('user_profile',views.user_profile_page),
    path('user_edit_profile',views.user_edit_profile),
    path('challenge_exam',views.challenge_exam),
    path('timer_exam',views.timer_exam),
    path('user_exam_code',views.user_exam_code),
    path('exam_loader',views.exam_loader),
    path('user_exam_execute',views.user_exam_execute),
    path('forgot_p',views.forgot_p),
    path('send_otp',views.send_otp),
    path('py_doc',views.py_doc)
]