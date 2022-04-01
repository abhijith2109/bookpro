from django.urls import path
from customer import views


urlpatterns=[
    path("home",views.customerIndex.as_view(),name="custhome"),
    path("accounts/register",views.SignUpView.as_view(),name="signup"),
    path("accounts/login",views.SiginInView.as_view(),name="signin"),
    path("accounts/logout",views.signout,name="signout"),
    path("accounts/password/reset",views.PasswordResetView.as_view(),name="passwordreset"),
]