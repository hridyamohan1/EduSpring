from django.shortcuts import render,redirect
from django.utils.termcolors import color_names
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.utils.crypto import get_random_string
from  django.core.mail import send_mail
from django.conf import settings
import razorpay
from .bform import *


# Create your views here.
def display(request):
    if request.method == 'GET':
        d = adcourse.objects.all()
        e = tutor.objects.filter(action="confirm")
        return render(request, 'index.html', {'r': d,'e':e})
    else:
        return render(request, 'index.html')

def signIn(request):
    if request.method == 'POST':
        u = request.POST['n1']
        p = request.POST['n2']
        try:
            data = login.objects.get(uname=u)
            if data.pswd == p:
                if data.usertype == 1:
                    request.session['a_id'] = u  #session created
                    return redirect(profile)
                elif data.usertype == 2:
                    data1 = tutor.objects.get(uname=u)
                    if data1.action == 'confirm':
                        request.session['t_id'] = u
                        return redirect(profile)
                    else:
                        messages.info(request, 'login failed,request is processing...')
                        return render(request, 'sign.html')
                elif data.usertype == 3:
                    request.session['u_id'] = u
                    return redirect(profile)
            else:
                messages.info(request,"Password incorrect")
                return render(request,'sign.html')
        except Exception:
            messages.info(request, "Username incorrect")
            return render(request,'sign.html')
    else:
        return render(request,'sign.html')


def adminindex(request):
    return render(request,'adminindex.html')

def teacherindex(request):
    u = request.session['t_id']
    d = tutor.objects.filter(uname=u)
    return render(request,'teacherindex.html',{'r':d})

def userindex(request):
    if request.method=='GET':
        a = request.session['u_id']
        d=user.objects.filter(uname=a)
        print(d)
    return render(request,'userindex.html',{'r':d})



def profile(request):
    if 'a_id' in request.session:    #session check
        u = request.session['a_id']
        d = login.objects.filter(uname=u)
        return render(request, 'adminindex.html')
    elif 't_id' in request.session:  # session check
        u = request.session['t_id']
        d = tutor.objects.filter(uname=u)
        return render(request, 'teacherindex.html',{'r': d})
    elif 'u_id' in request.session:
        u = request.session['u_id']
        d = user.objects.filter(uname=u)
        return render(request, 'userindex.html',{'r': d})
    else:
        return render(request,'index.html')




# def profile1(request):
#     if 't_id' in request.session:    #session check
#         u = request.session['t_id']
#         d = tutor.objects.filter(uname=u)
#         return render(request, 'teacherindex.html')
#     else:
#         return render(request,'index.html')


def signUp(request):
    if request.method == 'POST':
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        e = request.POST['n5']
        f = request.POST['n6']
        g = request.FILES['n7']
        h = request.POST['n8']
        # i = request.POST['n9']
        j = request.POST['n10']
        k = request.FILES['n11']
        u = request.POST['n12']
        p = request.POST['n13']
        data1 = tutor.objects.filter(uname=u)
        data2 = tutor.objects.filter(email=c)
        data3 = tutor.objects.filter(phone=d)
        if data1.exists():
            url = 'signup'
            msg = '''<script>alert('Username already exist')
                                            window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
        elif data2.exists():
            url = 'signup'
            msg = '''<script>alert('email already exist')
                                                        window.location='%s'</script>''' % (url)
            return HttpResponse(msg)

        elif data3.exists():
            url = 'signup'
            msg = '''<script>alert('Phone Number already exist')
                                         window.location='%s'</script>''' % (url)
            return HttpResponse(msg)

        else:
            data = tutor.objects.create(f_name=a,l_name=b,email=c,phone=d,age=e,address=f,img=g,qualification=h,course=j,cv=k,uname=u,pswd=p,action="pending")
            data1 = login.objects.create(uname=u,pswd=p,usertype=2)
            data.save()
            data1.save()
            url = 'signup'
            msg = '''<script>alert('Registration Successfull...Wait for admin approval to login')
                                window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
            # return redirect(signIn)
            # messages.success(request,"Registration successful")
    else:
        return render(request,'teacher_signup.html')



def usersignup(request):
    if request.method == 'POST':
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        e = request.POST['n5']
        f = request.FILES['n6']
        u = request.POST['n7']
        p = request.POST['n8']
        data1 = user.objects.filter(uname=u)
        if data1.exists():
            messages.info(request, "Username already exist")
            return render(request, 'index.html')
        else:
            data = user.objects.create(f_name=a, l_name=b, email=c, phone=d, age=e,img=f,uname=u, pswd=p)
            data1 = login.objects.create(uname=u, pswd=p, usertype=3)
            data.save()
            data1.save()
            url = 'sign'
            msg = '''<script>alert('Registration Successfull')
                                        window.location='%s'</script>''' % (url)
            return HttpResponse(msg)
            # return redirect(signIn)
            # messages.success(request,"Registration successful")
    else:
        return render(request, 'user_signup.html')


def logout(request):
    if 'a_id' in request.session:
        request.session.flush()
        return redirect(display)
    elif  't_id' in request.session:
        request.session.flush()
        return redirect(display)
    else:
        request.session.flush()
        return redirect(display)


def course(request):
    return render(request,'admin_course.html')

def program(request):
    return render(request,'admin_program.html')

def teacher(request):
    return render(request,'admin_teacher.html')

def student(request):
    return render(request,'admin_student.html')

def t_student(request):
    return render(request,'teacher_student.html')

def t_program(request):
    return render(request,'teacher_program.html')

# def t_profile(request):
#     return render(request,'teacher_profile.html')

def u_course(request):
    return render(request, 'user_course.html')

def u_program(request):
    return render(request, 'user_program.html')

def u_home(request):
    if request.method=='GET':
        a = request.session['u_id']
        d=user.objects.filter(uname=a)
        print(d)
    return render(request,'user_home.html',{'r':d})


def addcourse(request):
    if request.method == 'POST':
        a = request.POST['n1']
        b = request.POST['n2']
        c = request.POST['n3']
        d = request.POST['n4']
        data = adcourse.objects.create(cname=a,duration=b,amount=c,date=d)
        data.save()
        url = 'addcourse'
        msg = '''<script>alert('Course added Successfully')
                                        window.location='%s'</script>''' % (url)
        return HttpResponse(msg)

    return render(request,'admin_addcourse.html')


def admin_addteacher(request):
    if request.method=='GET':
         d=tutor.objects.filter(action='pending')
         return render(request,'admin_adteacher.html',{'r':d})
    else:
        return render(request,'admin_adteacher.html')

def view_adteacher(request):
    if request.method=='GET':
         d=tutor.objects.filter(action='confirm')
         return render(request,'admin_viewteacher.html',{'r':d})
    else:
        return render(request,'adminindex.html')

def admin_update(request):
    if request.method=='POST':
        a = request.POST['b1']
        b = request.POST['b2']
        d = tutor.objects.filter(uname=a)
        d.update(action='confirm')
        send_mail('Approval', 'Your registration is approved by the admin...Now you can login by your username and password',
                  settings.EMAIL_HOST_USER, [b], fail_silently=False)
        return redirect(admin_addteacher
                        )
    else:
        return render(request,'admin_adteacher.html')


def admin_delete(request):
    if request.method=='POST':
        a = request.POST['b2']
        print(a)
        # token = get_random_string(length=4)
        d = tutor.objects.get(email=a)

        # email = request.POST.get('email')
        # u = tutor.objects.get(email=email)
        # b= d.email
        d.delete()
        send_mail('Reject', 'your registration is rejected',
                  settings.EMAIL_HOST_USER, [a], fail_silently=False)
        return render(request, 'admin_adteacher.html')
    else:
        return render(request,'admin_adteacher.html')



def admin_viewcourse(request):
    if request.method=='GET':
         d=adcourse.objects.all()
         return render(request,'admin_viewcourse.html',{'r':d})
    else:
        return render(request,'admin_course.html')


def admin_course_delete(request):
    if request.method=='POST':
        a = request.POST['b2']
        print(a)
        d = adcourse.objects.filter(cname=a)
        d.delete()
        return redirect(admin_viewcourse)
    else:
        return render(request,'admin_course.html')


def admin_view_students(request):
    if request.method=='GET':
         d=user.objects.all()
         return render(request,'admin_viewstudents.html',{'r':d})
    else:
        return render(request,'admin_student.html')


def  admin_complaint(request):
    if request.method == 'GET':
        d = gethelp.objects.all()
    return render(request,'admin_complaint.html',{'r':d})


def admin_reply(request,u):
    if request.method == 'POST':
        b = request.POST['n1']
        data = gethelp.objects.filter(uname=u)
        print(data)
        data.update(action=b)
        url = 'sendcomp'
        msge = '''<script>alert('Reply send Successfully')
                                                    window.location='%s'</script>''' % (url)
        return HttpResponse(msge)
    else:
        return render(request,'admin_reply.html',{'uname':u})


def admin_sendmsg(request):
    if request.method == 'POST':
        b = request.POST['n1']
        a = request.session['a_id']
        data = tutor.objects.filter(uname=a)
        data.update(msg=b)
        return render(request,'admin_sendmsg.html')
    return render(request,'admin_sendmsg.html')


def admin_paymenthistory(request):
    if request.method=='GET':
        a = request.session['a_id']
        d=payment.objects.all()
        return render(request,'admin_paymenthistory.html',{'r':d})
    else:
        return render(request,'admin_paymenthistory.html')

def teacher_profile(request):
    if request.method == 'GET':
        a = request.session['t_id']
        data = tutor.objects.filter(uname=a)
        print(data)
        return render(request, 'teacher_profile.html', {'r': data})
    return render(request, 'teacher_profile.html')


# def teacher_updateprofile(request):
#     if request.method == 'GET':
#         a = request.session['t_id']
#         data = tutor.objects.filter(uname=a)
#         # return render(request, 'profile.html', {'r': data})
#         return render(request, 'teacher_update_profile.html', {'r': data})
#     else:
#         return render(request, 'teacher_profile.html')


def teacher_update_profile(request,id):
    if 't_id' in request.session:
        data = tutor.objects.get(pk=id)
        f = teacherform(instance = data)
        if request.method == 'POST':
             f = teacherform(request.POST, request.FILES, instance = data)
             if f.is_valid():
                 f.save()
                 messages.success(request,'Updated successfully')
                 return redirect(teacher_profile)
             return redirect(teacher_profile)
        return render(request, 'teacher_update_profile.html', {'data': data,'f':f})
    else:
        return redirect(userindex)


def teacher_paymenthistory(request,u):
    request.session['s_uname'] = u
    print(u)
    d = payment.objects.filter(uname=u)
    print(d)
    return render(request, 'teacher_paymenthistory.html',{'r':d})


def user_viewcourse(request):
    if request.method=='GET':
         a = request.session['u_id']
         print(a)
         d=adcourse.objects.all()
         s=set()
         for i in d:
             s.add(i.cname)
         l=list(s)
         print(l)
         # f = courseregister.objects.all()
         # print(f)
         # for i in f:
         #     print(i.cname)
         f = courseregister.objects.filter(uname=a)  # a is session user_id
         registered_courses = set(i.cname for i in f)
         print(registered_courses)
         return render(request,'user_viewcourse.html',{'r':d,'r1':l,'f': registered_courses})
    else:
        return render(request,'user_course.html')

def user_searchcourse(request):
    if request.method == 'POST':
        x = request.POST['f1']
        d = adcourse.objects.filter(cname=x)
        a = request.session['u_id']
        print(a)
        f = courseregister.objects.filter(uname=a)  # a is session user_id
        registered_courses = set(i.cname for i in f)
        print(registered_courses)
        return render(request, 'user_viewcourse.html',{'r':d,'f': registered_courses})
    else:
       return render(request, 'user_viewcourse.html')


def user_course_register(request):
    if request.method == 'POST':
        a = request.POST['b2']
        print(a)
        d = adcourse.objects.get(cname=a)
        return render(request,'user_courseregister.html',{'r':d})
    else:
        return render(request,'user_course.html')


def userprofile(request):
    if request.method == 'GET':
        a = request.session['u_id']
        data = user.objects.filter(uname=a)
        return render(request, 'user_profile.html', {'r': data})
    else:
         return render(request, 'userindex.html')

# def update_profile(request,id):
#     data = user.objects.get(pk=id)
    #     if request.method == 'GET':
#         a = request.session['u_id']
#         data = user.objects.filter(uname=a)
#         # return render(request, 'profile.html', {'r': data})
#     return render(request, 'update_profile.html', {'r': data})
#     else:
#         return render(request, 'user_profile.html')


def up_prof(request,id):
    if 'u_id' in request.session:
        data = user.objects.get(pk=id)
        f = modelform(instance = data)
        if request.method == 'POST':
             f = modelform(request.POST, request.FILES, instance = data)
             if f.is_valid():
                 f.save()
                 messages.success(request,'Updated successfully')
                 return redirect(userprofile)
             return redirect(userprofile)
        return render(request, 'update_profile.html', {'data': data,'f':f})
    else:
        return redirect(userindex)

def coursereg(request):
    return render(request,'payment.html')


def user_help(request):
    return render(request, 'user_help.html')

def help(request):
    if request.method == 'POST':
        b = request.POST['n1']
        a = request.session['u_id']
        data = user.objects.filter(uname=a)
        data1 = gethelp.objects.create(uname=a,msg=b,action="pending")
        data1.save()
        url = 'sendcomp'
        msge = '''<script>alert('Complaint send Successfully')
                                                window.location='%s'</script>''' % (url)
        return HttpResponse(msge)

    return render(request,'help.html')


def viewcomplaint(request):
    if request.method == 'GET':
        a = request.session['u_id']
        d = gethelp.objects.filter(uname=a)
        return render(request,'user_viewcomplaint.html',{'r':d})

    return render(request,'user_viewcomplaint.html',)

def changepswd(request):
    # request.session['s_uname'] = u
    # print(u)
    return render(request,'user_changepswd.html')

def chpassword(request):
    if request.method == 'POST':
        d = request.POST['n3']
        e = request.POST['n1']
        f = request.POST['n2']
        data = user.objects.filter(uname=d)
        if data.exists():
            data.update(pswd=f)
        else:
            url = 'change'
            msge = '''<script>alert('Username does not exist')
                                                                window.location='%s'</script>''' % (url)
            return HttpResponse(msge)

        data = login.objects.filter(uname=d,pswd=e)
        if data.exists():
            data.update(pswd=f)
        else:
            url = 'change'
            msge = '''<script>alert('Username does not exist')
                                                            window.location='%s'</script>''' % (url)
            return HttpResponse(msge)
        return redirect(signIn)
    return render(request, 'user_changepswd.html')

def teacher_change_password(request):
    return render(request, 'teacher_change_password.html')

def teacher_changepssrd(request):
    if request.method == 'POST':
        d = request.POST['n3']
        e = request.POST['n1']
        f = request.POST['n2']
        print(d)
        data = tutor.objects.filter(uname=d)
        data.update(pswd=f)
        data = login.objects.filter(uname=d, pswd=e)
        data.update(pswd=f)
        # url = 'change'
        # msge = '''<script>alert('Password changed Successfully')
        #                                                 window.location='%s'</script>''' % (url)
        # return HttpResponse(msge)
        return redirect(signIn)
    return render(request, 'teacher_change_password.html')




def teacher_help(request):
    return render(request,'teacher_gethelp.html')


def teacher_viewcomp(request):
    if request.method == 'POST':
        b = request.POST['n1']
        a = request.session['t_id']
        data = tutor.objects.filter(uname=a)
        data1 = gethelp.objects.create(uname=a,msg=b,action="pending")
        data1.save()
        url = 'tsndcomp'
        msge = '''<script>alert('Complaint send Successfully')
                                                window.location='%s'</script>''' % (url)
        return HttpResponse(msge)

    return render(request, 'teacher_viewcomplaint.html')


def teacher_viewreply(request):
    if request.method == 'GET':
        a = request.session['t_id']
        d = gethelp.objects.filter(uname=a)
    # return render(request,'user_viewcomplaint.html',{'r':d})

    return render(request, 'teacher_viewreply.html',{'r':d})


def teacher_viewstudents(request):
    a = request.session['t_id']
    print(a)
    b = tutor.objects.get(uname=a)
    print(b)
    c = courseregister.objects.filter(cname=b.course)
    print(c)
    l=[]
    for i in c:
        print(i.uname)
        data=user.objects.get(uname=i.uname)
        print(data.email)
        l.append(data)
    print(l)
        # d = courseregister.objects.filter(cname=c)
    return render(request,'teacher_viewstudent.html',{'data':l})

def teacher_tutoring(request,u):
    request.session['s_uname'] = u
    print(u)
    # data = user.objects.get(uname=u)
    # print(data)
    return render(request,'teacher_tutoring.html',)

def teacher_uploadsession(request):
    if request.method == 'POST':
        a = request.session['t_id']
        print(a)
        t = tutor.objects.filter(uname=a)
        for i in t:
            j = i.course
            print(j)
        d = request.POST['n1']
        b = request.POST['n2']
        c = request.FILES['n3']
        data = request.session['s_uname']
        print(data)
        data1 = session.objects.create(uname=data,topic=d, link=b, notes=c,course=j)
        data1.save()
        url = 'upload'
        msge = '''<script>alert('Session uploaded Successfully')
                                                        window.location='%s'</script>''' % (url)
        return HttpResponse(msge)
    return render(request, 'teacher_uploadsession.html')

def teacher_viewsession(request):
    if request.method == 'GET':
        # a = request.session['t_id']
        u = request.session['s_uname']
        print(u)
        d = session.objects.filter(uname=u)
        return render(request,'teacher_viewsession.html',{'r':d})
    return render(request, 'teacher_viewsession.html')

def pay(request,amount,id):
    amt = amount* 100
    request.session['amount'] = id
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    # cursor = connection.cursor()
    # cursor.execute(
    #     "update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(
    #         id) + "' ")

    # payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "pay.html", {'r': amt,'id':id})


def successpay(request):
    if request.method == 'POST':
        a = request.session['u_id']
        id=request.POST['n1']
        print(id)
        c = user.objects.filter(uname=a)
        adcourse_instance = adcourse.objects.get(pk=id)
        print("******",adcourse_instance)
        b=adcourse_instance.cname
        request.session['cname']=b
        print("_______________________________")
        print(b)
        d=adcourse_instance.duration
        f=adcourse_instance.amount
        print(b)
        print(d)
        # data1 = courseregister.objects.get(pk=i)

        # Save course registration
        data1 = courseregister.objects.create(uname=a,cname=b,amount=f,date=timezone.now(),ad_amount=1000,duration=d)
        data1.save()
        d = courseregister.objects.filter(uname=a)
        l = []
        for i in d:
            l.append(i)
        print("____________________---")
        print(l)
        for i in l:
            data = payment.objects.create(uname=a,amount=1000,status="paid",course_details=i)

            data.save()
            l.clear()
        print("____________________---")
        print(l)
        return render(request, 'user_course.html',{'r':d})
    else:
        return redirect(u_course)


def user_payment_history(request):
    if request.method=='GET':
        a = request.session['u_id']
        d=payment.objects.filter(uname=a)
        return render(request,'user_paymenthistory.html',{'r':d})
    else:
        return render(request, 'user_paymenthistory.html')


def user_mycourse(request):
    if request.method=='GET':
        a = request.session['u_id']
        d=courseregister.objects.filter(uname=a)
        s = 0
        l=[]
        for i in d:
            print(i.amount)
            s = i.amount
            print("**********88")
            print(i.cname)
            l.append(i.cname)
        print(s)
        request.session['amount'] = s
        print(l)
        # co=courseregister.objects.get(cname='python')
        # print(co.payment_status)
        co=True
        return render(request, 'user_mycourse.html',{'r':d,'z':s,'data':co})
    else:
        return render(request,'user_mycourse.html')
    

def user_startlearn(request,u):
    if request.method=='GET':
        a = request.session['u_id']
        request.session['cname'] = u
        print(u)
        d=session.objects.filter(uname=a,course=u)
        return render(request,'user_startlearn.html',{'r':d})

def user_pay(request,cname,amount):
    request.session['course']=cname
    amt = amount * 100
    # request.session['amount'] = id
    order_currency = 'INR'
    client = razorpay.Client(
        auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))
    # cursor = connection.cursor()
    # cursor.execute(
    #     "update inspection_details set status='completed', fine_paid_date = curdate() where insp_id='" + str(
    #         id) + "' ")

    # payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    return render(request, "user_pay.html", {'r': amt})

def success1(request):
    if request.method == 'POST':
        a = request.session['u_id']
        s = request.session['amount']
        print(a)
        a = request.session['u_id']
        d = courseregister.objects.get(cname=request.session['course'],uname=a)
        print(d)
        data = payment.objects.create(uname=a,amount=d.amount,status="paid",course_details=d)
        data.save()

        d.payment_status = True
        d.save()
        # l=[]
        # for i in d:
        #     l.append(i)
        # print(l)
        # for i in l:
        #     data = payment.objects.create(uname=a,amount=i.amount,status="paid",course_details=i)
        #     data.save()
        #     d = courseregister.objects.get(cname=request.session['cname'])
        #     d.payment_status = True
        #     d.save()
        print("__________2payment_______________")
        print(d)
        return redirect(user_mycourse)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)
        try:
            u = user.objects.get(email=email)
        except Exception:
            messages.info(request,"Email id not registered")
            return render(request, 'forgot.html')
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=u, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:4000/reset/{token}'

        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'forgot.html')

def reset_password(request, token):
    print("jsdgfkhdgfkjdgfkdj")
    # Verify token and reset the password
    password_reset = PasswordReset.objects.get(token=token)
    print(password_reset)
    # usr = user.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('n1')
        repeat_password = request.POST.get('n2')
        if repeat_password == new_password:
            u = password_reset.user.uname
            login.objects.filter(uname=u).update(pswd=new_password)
            user.objects.filter(uname=u).update(pswd=new_password)


            # password_reset.user.password=new_password
            # password_reset.user.save()

            # # password_reset.delete()
            return redirect(signIn)
    return render(request, 'reset.html',{'token':token})





