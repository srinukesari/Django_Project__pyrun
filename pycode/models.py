from django.db import models
from django.contrib.postgres.fields import ArrayField

class questions(models.Model):
    type=(
        ('Easy','easy'),
        ('medium','Medium'),
        ('hard','Hard'),
        ('advance','Advance')
    )
    question_name = models.CharField(max_length=100)
    question_type = models.CharField(max_length=10, choices=type, default='easy')
    question_score = models.IntegerField()
    question_code = models.IntegerField(default=3950, unique=True)
    problem = models.TextField(default=None)
    input_format = models.TextField(default=None)
    output_format = models.TextField(default=None)
    constraints = models.TextField(default=None)
    sample_input = models.TextField(default=None)
    sample_output = models.TextField(default=None)
    explanation = models.TextField(default=None)



class challenges(models.Model):
    challenge_name = models.CharField(max_length= 30)
    challenge_code = models.IntegerField()
    challenge_type = models.CharField(max_length=20)
    challenge_image = models.ImageField(upload_to="challenge_pics")
    type_algo =models.CharField(max_length=40,null=True)
    ctc = models.CharField(max_length=30,null=True,default='Best in Industry')
    job_role = models.CharField(max_length=30,null=True,default='not mentioned')
    yop = models.CharField(max_length=20,null=True)
    about = models.TextField(null=True)
    format = models.TextField(null=True)
    location = models.TextField(null=True)
    openings = models.TextField(null=True)
    ques_code = models.TextField(null=True)
    exam_time = models.IntegerField(null=True)

class test_cases(models.Model):
    ques_code = models.IntegerField(unique=True)
    test_case_inputs = models.TextField()
    test_case_outputs = models.TextField()



class user_profile(models.Model):

    profile_username = models.CharField(max_length=30,primary_key=True)
    education = models.CharField(max_length=50,default='Not Mentioned',null = True)
    skill = models.CharField(max_length=50,default='C',null= True)
    ques_solved = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='profile_pics',default='null',null = True,blank = True)
    linkedin = models.TextField(default='add link',null=True)
    github = models.TextField(default='add link',null=True)
    facebook = models.TextField(default='add link',null=True)
    twiter = models.TextField(default='add link',null=True)
    mobile = models.BigIntegerField(default=0000000000)
    whatsapp = models.BigIntegerField(default=0000000000)



