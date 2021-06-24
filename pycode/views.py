from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import questions,challenges,test_cases ,user_profile
from subprocess import *
import subprocess
import re
from time import time
import random




def home_quote(request):
    return render(request,'home_quote.html')

def user_challenges(request):
    challenge = challenges.objects.all()
    return render(request,'user_challenges.html',{'challenge':challenge,'url':'uc'})

def user_practise(request):
    ques = questions.objects.all()
    if request.method == 'POST':
        easy = request.POST.get('easy')
        medium = request.POST.get('medium')
        hard = request.POST.get('hard')
        advance = request.POST.get('advance')
        print(easy)
        print(medium)
        print(hard)
        print(advance)
        ques = questions.objects.none()
        if easy:
            ques |= questions.objects.filter(question_type = 'Easy')
        if medium:
            ques |= questions.objects.filter(question_type='medium')
        if hard:
            ques |= questions.objects.filter(question_type='hard')
        if advance:
            ques |= questions.objects.filter(question_type='advance')

        context_checkbox={'questions':ques,'easy':easy,'medium':medium,'hard':hard,'advance':advance}
        return render(request,'user_practise.html',context_checkbox)
    else:
        try:
            del request.session['end_time']
        except KeyError:
            pass
        return render(request,'user_practise.html',{'questions':ques,'url':'up'})

def user_solve(request):
    code = request.POST['code']

    regex = re.compile(r'[\r]')
    code = regex.sub("", code)

    code = list(map(str,code.split(",")))
    code[0] = code[0][1:]
    code[10] = code[10][:-1]

    for i in range(len(code)):
        code[i] = code[i].strip()


    context = {
        'question_name':code[0], 'question_type':code[1],
        'question_score':code[2], 'question_code':code[3],
        'code':code[4],'input_format':code[5],
        'output_format':code[6],'constraints':code[7],
        'sample_input':code[8],'sample_output':code[9],
        'explanation':code[10],'code_submitedd':""
    }
    return render(request,'user_solve.html',context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)

        print(user)

        if user is None:
            print("coming here")
            messages.error(request, 'Login_failed')
            return redirect('/login')
        else:
            auth.login(request, user)
            request.session['ss_user'] = username
            request.session['exam_flag'] = 0
            request.session['flag']=0
            messages.success(request, 'Login_Successfully')
            return redirect('/user_practise')

    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout_Successfully')
    return redirect('/home_quote')
def signup(request):
    if request.method =="POST":
        user = request.POST.get('username')
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username = user).exists():
            print('user name exits')
            messages.info(request,"username taken please try with another Username")
            return HttpResponseRedirect('/signup')
        elif User.objects.filter(email = email).exists():
            messages.info(request, "Email is already Registered Please go to login page!!!")
            return redirect('/signup')
        else:
            subject = "Pyrun Official"
            message = 'Greetings from Pyrun Community!!!\n we are glad that you are now part of Pyrun Society.\n\n\n'
            message += 'Explore Python ...!!!\n make yourself comfortable with Python...\n\n\nThanks&regards\nPyrun-Team'
            res = send_mail(subject, message,email,[email])
            if res:
                user_obj = User.objects.create_user(username=user,email=email,password=password)
                user_obj.save()
                messages.success(request, 'Successfully Registered')
                print(user)
                profile = user_profile(profile_username = user)
                profile.save()
                print("user created")
                return redirect('/home_quote')
            else:
                messages.error(request,'email is not valid!!! check it once.')
                return redirect('/signup')
    else:
        return render(request,'signup.html')

def loader(request):
    code_area = request.POST['code_area']
    code_str = request.POST['code_solve']

    custom_check = request.POST.get('custom_check', False)
    custom_input = request.POST['custom_in']
    run_sub = request.POST['run']
    print(run_sub)
    context_load = {'code_area':code_area,'code_str':code_str,
               'custom_check':custom_check,'custom_input':custom_input,
               'run_sub':run_sub
    }
    request.session['session_context'] = context_load
    return render(request,'loader.html',{'run_sub':run_sub})


def user_execute(request):
    context_loader = request.session.pop('session_context', None)
    print(context_loader)
    code_area = context_loader['code_area']
    code_str = context_loader['code_str']

    custom_check = context_loader['custom_check']
    custom_input = context_loader['custom_input']

    run_sub = context_loader['run_sub']


    test_cases_result = []
    test_cases_error = ""

    print(run_sub)
    print(custom_check)
    print(custom_input)

    regex = re.compile(r'[\r]')
    code_str = regex.sub("",code_str)

    code = list(map(str, code_str.split(",")))

    code[0] = code[0][1:]
    code[10] = code[10][:-1]
    for i in range(len(code)):
        code[i] = code[i].strip()

    file = open('python_code_area.py', 'w')
    file.write(code_area)
    file.close()
    print(code[8:10])

    if run_sub == "run":
            #print(code[9])
        if custom_check == 'true':
            with open("input", 'w', newline='\n') as file:
                file.write(custom_input)
        else :
            with open("input", 'w', newline='\n') as file:
                file.write(code[8])
            #call(['python3', 'python_code_area.py'])
            #p = Popen(['python3', 'python_code_area.py'],stdin=PIPE,stdout=PIPE, stderr=PIPE)
            #stdout, stderr = p.communicate()
        with open('input','r') as f_in:
            p = subprocess.run(['python3', 'python_code_area.py'],stdin=f_in,stdout=PIPE,stderr=PIPE)
        print(p.returncode)
        msg = 'error occured'
        pro_error = 'no error'
        output = 'error occured'
        ans =''
        flag = -1

        if p.returncode == 0:
            output = p.stdout.decode().strip()
            msg = 'Compilation Sucessfull :)'
            if output == code[9]:
                flag = 1
                ans = 'Correct Answer :)'
                print("crct ans")
            else:
                flag = 0
                ans = 'Wrong Answer :('
                print("wrng")
        else:
            msg = 'Compilation failed :('
            pro_error = p.stderr.decode().strip()
            print(pro_error)

        context = {
                'question_name': code[0], 'question_type': code[1],
                'question_score': code[2], 'question_code': code[3],
                'code': code[4], 'input_format': code[5],
                'output_format': code[6], 'constraints': code[7],
                'sample_input': code[8], 'sample_output': code[9],
                'explanation': code[10],'msg':msg,
                'exec_output': output,'exec_error':pro_error,'code_submited':code_area,
                'ans':ans,'flag':flag,'return_code':p.returncode,'check_status':custom_check,
                'custom_input':custom_input,'run_sub':run_sub,'test_cases_result':test_cases_result,
                'test_cases_error':test_cases_error,'run_sub':run_sub
            }
        print(custom_check)
        return render(request,'user_execute.html',context)
    else:
        ts = test_cases.objects.filter(ques_code = code[3]).get()
        ts_inputs = list(map(str,ts.test_case_inputs.split("$")))
        ts_outputs = list(map(str,ts.test_case_outputs.split("$")))
        ts_results = []
        print(ts_inputs)
        print(ts_outputs)
        for i in range(len(ts_inputs)):
            with open("input", 'w', newline='\n') as file:
                file.write(ts_inputs[i])
            with open('input', 'r') as f_in:
                p = subprocess.run(['python3', 'python_code_area.py'], stdin=f_in, stdout=PIPE, stderr=PIPE)
            print(p.returncode)
            if p.returncode == 0:
                res_output = p.stdout.decode().strip()
                if res_output == ts_outputs[i]:
                    ts_results.append(1)
                else:
                    ts_results.append(0)
            else:
                ts_results.append(-1)
        print(ts_results)
        ts_passed = ts_results.count(1)

        context = { 'question_name': code[0], 'question_type': code[1],
                'question_score': code[2], 'question_code': code[3],
                'code': code[4], 'input_format': code[5],
                'output_format': code[6], 'constraints': code[7],
                'sample_input': code[8], 'sample_output': code[9],
                'explanation': code[10],'ts_results':ts_results,'run_sub':run_sub,
                'ts_passed':ts_passed,'ts_len':len(ts_results),'code_submited':code_area
        }
        return render(request,"user_execute.html",context)


def user_profile_page(request):
    if request.method == 'POST':
        up_user = request.session.pop('ss_user', None)
        request.session['ss_user'] = up_user
        print(up_user)
        edu = request.POST['education']
        skill = request.POST['skill']
        linkedin = request.POST['linkedin']
        git = request.POST['github']
        fb = request.POST['facebook']
        twiter  = request.POST['twiter']
        mobile =request.POST['mobile']
        whatsapp = request.POST['whatsapp']
        user_profile_input = request.FILES.get('profile_img')
        print(user_profile_input)
        print("check upper")
        if user_profile_input == None:
            up_update = user_profile(education = edu,skill = skill,linkedin = linkedin,
                                    github = git,facebook = fb,twiter = twiter,
                                    mobile= mobile,whatsapp = whatsapp
                                    ,profile_username = up_user)
            up_update.save(update_fields=['education','skill','linkedin','github','facebook'
                ,'twiter','whatsapp','mobile'])
        else:
            up_update = user_profile(education=edu, skill=skill, linkedin=linkedin,
                                     github=git, facebook=fb, twiter=twiter,
                                     mobile=mobile, whatsapp=whatsapp,profile_pic = user_profile_input
                                     , profile_username=up_user)
            up_update.save()

    print(request.method)
    ss_user=request.session.pop('ss_user', None)
    request.session['ss_user'] = ss_user

    print(ss_user)
    profile_obj = user_profile.objects.filter(profile_username = ss_user).get()
    if bool(profile_obj.profile_pic):
        bool_pic = 1
    else:
        bool_pic = 0

    return render(request,'user_profile.html',{'profile_obj':profile_obj,'bool_pic':bool_pic})



def user_edit_profile(request):
    ss_user = request.session.pop('ss_user', None)
    request.session['ss_user'] = ss_user

    print(ss_user)
    profile_obj = user_profile.objects.filter(profile_username=ss_user).get()
    if bool(profile_obj.profile_pic):
        bool_pic = 1
    else:
        bool_pic = 0
    return render(request,'user_edit_profile.html',{'profile_obj':profile_obj,'bool_pic':bool_pic})

def challenge_exam(request):
    cha_code = request.POST['cha_code']
    print(cha_code)
    exam_page = challenges.objects.filter(challenge_code = cha_code)
    return render(request,'user_cha_exam.html',{'exam_page':exam_page})

def timer_exam(request):
    global exam_flag
    if request.session['exam_flag'] ==0 :
        exam_code = request.POST['exam_code']
        request.session['exam_code'] = exam_code
        request.session['exam_flag'] = 1
    else:
        exam_code = request.session['exam_code']
    exam_obj = challenges.objects.filter(challenge_code = exam_code)
    p=[]
    for i in exam_obj:
        print(i.ques_code)
        p = list(map(int,i.ques_code.split(",")))
        print(p)
        timer= i.exam_time

    que_obj = questions.objects.none()
    print("checkkkkkk")
    print(request.session['flag'])

    if 'end_time' not in request.session:
        request.session['flag'] = 0
    if request.session['flag'] == 0:
        end_time = int(timer) + int(time() * 1000)
        end_time = float(end_time)
        print(end_time)
        request.session['flag'] = 1
        request.session['end_time'] = end_time
        print(request.session['end_time'])
        print(end_time-timer)
    else:
        try:
            print(request.session['end_time'])
            end_time = request.session['end_time']
        except KeyError:
            print("from else")

    for i in p:
        que_obj |= questions.objects.filter(question_code=i)
    print(end_time)
    end_time = float(end_time)
    print(type(end_time))
    print(type(time()*1000))
    print(end_time - int(time() * 1000))
    return render(request, 'user_timer_ques.html', {'que_obj': que_obj, 'timer': end_time - int(time() * 1000)})


def user_exam_code(request):
    code = request.POST['code']
    end_time = request.session.pop('end_time', None)
    request.session['end_time'] = end_time
    ques = questions.objects.filter(question_code = code)

    print(code)
    context_sent={}
    for q in ques:
        context_sent['question_name']=q.question_name
        context_sent['question_code']=q.question_code
        context_sent['problem']=q.problem
        context_sent['input_format']=q.input_format
        context_sent['output_format']=q.output_format
        context_sent['constraints']=q.constraints
        context_sent['sample_input'] = q.sample_input
        context_sent['sample_output'] = q.sample_output
        context_sent['explanation'] = q.explanation
        context_sent['timer'] = end_time - int(time()*1000)
    return render(request,'user_timer_code.html',context_sent)

def exam_loader(request):
    code_area = request.POST['code_area']
    code_str = request.POST['code_solve']

    custom_check = request.POST.get('custom_check', False)
    custom_input = request.POST['custom_in']
    run_sub = request.POST['run']
    end_time = request.session.pop('end_time', None)
    request.session['end_time'] = end_time
    print(run_sub)
    context_load = {'code_area': code_area, 'code_str': code_str,
                    'custom_check': custom_check, 'custom_input': custom_input,
                    'run_sub': run_sub
                    }
    request.session['session_context'] = context_load
    return render(request, 'exam_loader.html', {'run_sub': run_sub,'timer':end_time - int(time()*1000)})


def user_exam_execute(request):
    context_loader = request.session.pop('session_context', None)
    print(context_loader)
    code_area = context_loader['code_area']
    code_str = context_loader['code_str']

    custom_check = context_loader['custom_check']
    custom_input = context_loader['custom_input']

    run_sub = context_loader['run_sub']
    end_time = request.session.pop('end_time', None)
    request.session['end_time'] = end_time

    test_cases_result = []
    test_cases_error = ""

    print(run_sub)
    print(custom_check)
    print(custom_input)

    regex = re.compile(r'[\r]')
    code_str = regex.sub("", code_str)

    code = list(map(str, code_str.split(",")))

    code[0] = code[0][1:]
    code[8] = code[8][:-1]
    for i in range(len(code)):
        code[i] = code[i].strip()

    file = open('python_code_area.py', 'w')
    file.write(code_area)
    file.close()

    if run_sub == "run":
        # print(code[9])
        if custom_check == 'true':
            with open("input", 'w', newline='\n') as file:
                file.write(custom_input)
        else:
            with open("input", 'w', newline='\n') as file:
                file.write(code[6])
            # call(['python3', 'python_code_area.py'])
            # p = Popen(['python3', 'python_code_area.py'],stdin=PIPE,stdout=PIPE, stderr=PIPE)
            # stdout, stderr = p.communicate()
        with open('input', 'r') as f_in:
            p = subprocess.run(['python3', 'python_code_area.py'], stdin=f_in, stdout=PIPE, stderr=PIPE)
        print(p.returncode)
        msg = 'error occured'
        pro_error = 'no error'
        output = 'error occured'
        ans = ''
        flag = -1

        if p.returncode == 0:
            output = p.stdout.decode().strip()
            msg = 'Compilation Sucessfull :)'
            if output == code[7]:
                flag = 1
                ans = 'Correct Answer :)'
                print("crct ans")
            else:
                flag = 0
                ans = 'Wrong Answer :('
                print("wrng")
        else:
            msg = 'Compilation failed :('
            pro_error = p.stderr.decode().strip()
            print(pro_error)

        context = {
            'question_name': code[0],'question_code': code[1],
            'problem': code[2], 'input_format': code[3],
            'output_format': code[4], 'constraints': code[5],
            'sample_input': code[6], 'sample_output': code[7],
            'explanation': code[8], 'msg': msg,
            'exec_output': output, 'exec_error': pro_error, 'code_submited': code_area,
            'ans': ans, 'flag': flag, 'return_code': p.returncode, 'check_status': custom_check,
            'custom_input': custom_input, 'run_sub': run_sub, 'test_cases_result': test_cases_result,
            'test_cases_error': test_cases_error, 'run_sub': run_sub,'timer':end_time - int(time()*1000)
        }
        print(custom_check)
        return render(request, 'user_execute_exam.html', context)
    else:
        ts = test_cases.objects.filter(ques_code=code[1]).get()
        ts_inputs = list(map(str, ts.test_case_inputs.split("$")))
        ts_outputs = list(map(str, ts.test_case_outputs.split("$")))
        ts_results = []
        print(ts_inputs)
        print(ts_outputs)
        for i in range(len(ts_inputs)):
            with open("input", 'w', newline='\n') as file:
                file.write(ts_inputs[i])
            with open('input', 'r') as f_in:
                p = subprocess.run(['python3', 'python_code_area.py'], stdin=f_in, stdout=PIPE, stderr=PIPE)
            print(p.returncode)
            if p.returncode == 0:
                res_output = p.stdout.decode().strip()
                if res_output == ts_outputs[i]:
                    ts_results.append(1)
                else:
                    ts_results.append(0)
            else:
                ts_results.append(-1)
        print(ts_results)
        ts_passed = ts_results.count(1)

        context = {'question_name': code[0],'question_code': code[1],
                   'problem': code[2], 'input_format': code[3],
                   'output_format': code[4], 'constraints': code[5],
                   'sample_input': code[6], 'sample_output': code[7],
                   'explanation': code[8], 'ts_results': ts_results, 'run_sub': run_sub,
                   'ts_passed': ts_passed, 'ts_len': len(ts_results), 'code_submited': code_area,
                   'timer':end_time - int(time()*1000)
                   }
        return render(request, "user_execute_exam.html", context)


def forgot_p(request):
    if request.method == "POST":
        otp = request.POST['otp']
        votp = request.POST['votp']
        print(otp)
        print(votp)
        if otp == votp:
            vemail = request.session.pop('email',None)
            new_pass = random.randint(1000000,9999999)
            subject = 'Pyrun Official'
            message = 'your new password for your account in pyrun is' + str(new_pass)
            message += '\n\n\n\nthansk & regards\nPyrun-Team'
            res = send_mail(subject, message, vemail, [vemail])
            username = request.session.pop('username',None)
            user_p = User.objects.get(username__exact= username)
            user_p.set_password(new_pass)
            user_p.save()
            if res:
                messages.success(request,'check your mail new password is sent to your mobile number')
                return redirect('/login')
            else:
                messages.error("network error!!!")
                return redirect('/login')
        else:
            messages.error(request,'Incorrect OTP!!!')
            return redirect('/login')
    else:
        return render(request,'forgot_p.html',{"set":0})

def send_otp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        user = User.objects.filter(username = username)
        if user is not None:
            user = User.objects.get(username = username)
            request.session['username'] = username
            if email == user.email:
                subject = 'Pyrun Official'
                otp = random.randint(1000,9999)
                message = 'your recovery Otp is'+str(otp)
                message +='\n\n\n\nthansk & regards\nPyrun-Team'
                res = send_mail(subject, message, email, [email])
                if res:
                    request.session['email'] = email
                    messages.success(request,'Otp sent succesfully to registered email!!!')
                    return render(request,'forgot_p.html',{'set':1,'otp':otp})
                else:
                    messages.error(request,'otp sent fail !!!')
                    return redirect('/login')
            else:
                messages.error(request,'Sorry! email is not matching with the registered email')
                return redirect('/login')
        else:
            messages.error(request,"username doesnot exists")
            return redirect('/login')

    messages.success(request,"succesfully msg sent!!!")

    return redirect('/home_quote')

def py_doc(request):
    return render(request,'py_doc.html')