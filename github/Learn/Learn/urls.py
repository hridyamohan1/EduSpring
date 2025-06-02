"""
URL configuration for Learn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('disp',views.display),
    path('sign',views.signIn),
    path('signup',views.signUp),
    path('usersignup',views.usersignup),
    path('',views.profile),
    # path('pro1',views.profile1),
    path('aindex',views.adminindex),
    path('tindex',views.teacherindex),
    path('uindex',views.userindex),
    path('logout',views.logout),
    path('course',views.course),
    path('program',views.program),
    path('teacher',views.teacher),
    path('student',views.student),
    path('student1',views.t_student),
    path('program1',views.t_program),
    # path('tprofile',views.t_profile),
    path('course2',views.u_course),
    path('program2',views.u_program),
    path('addcourse',views.addcourse),
    path('vateacher',views.view_adteacher),
    path('adteacher',views.admin_addteacher),
    path('adminupdate',views.admin_update),
    path('admindelete',views.admin_delete),
    path('viewcourse',views.admin_viewcourse),
    path('deletecourse',views.admin_course_delete),
    path('adpayment',views.admin_paymenthistory),
    path('viewstudents',views.admin_view_students),
    path('teacher_profile',views.teacher_profile),
    path('userviewcourse',views.user_viewcourse),
    path('courseregister',views.user_course_register),
    path('userprofile',views.userprofile),
    # path('updateprofile/<int:id>',views.update_profile),
    path('update_profile/<int:id>',views.up_prof),
    path('creg',views.coursereg),
    path('help',views.user_help),
    path('uhome',views.u_home),
    path('sendcomp',views.help),
    path('viewcomp',views.viewcomplaint),
    path('change',views.changepswd),
    path('chpswd',views.chpassword),
    path('teacherchange',views.teacher_change_password),
    path('teacherchpsrd',views.teacher_changepssrd),
    path('admincomp',views.admin_complaint),
    path('reply/<u>',views.admin_reply),
    path('admin_reply', views.admin_reply, name='admin_reply'),
    path('sendmsg',views.admin_sendmsg),
    # path('admintsnd',views.admin_teacher_snd),
    path('ghlp',views.teacher_help),
    path('tsndcomp',views.teacher_viewcomp),
    path('tviewreply',views.teacher_viewreply),
    path('pay/<int:amount>/<int:id>', views.pay),
    path('success',views.successpay),
    path('payhis',views.user_payment_history),
    path('mycourse',views.user_mycourse),
    path('viewstud',views.teacher_viewstudents),
    path('tedit/<int:id>',views.teacher_update_profile),
    path('start/<u>',views.teacher_tutoring),
    path('upload',views.teacher_uploadsession),
    path('viewsession',views.teacher_viewsession),
    path('startLearn/<u>',views.user_startlearn),
    path('fpay/<cname>/<int:amount>',views.user_pay),
    path('success1',views.success1),
    path('c',views.user_searchcourse),
    path('teacher_payment/<u>',views.teacher_paymenthistory),


    path('forgot',views.forgot_password,name="forgot"),
    path('reset/<token>',views.reset_password,name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)