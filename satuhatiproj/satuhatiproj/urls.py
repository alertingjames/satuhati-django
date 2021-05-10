from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from satuhati import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^satuhati/', include('satuhati.urls')),
    url(r'^$', views.index, name='index'),

    url(r'^signup',views.signup,  name='signup'),
    url(r'^signin',views.signin,  name='signin'),
    url(r'^forgotpassword', views.forgotpassword, name='forgotpassword'),
    url(r'^codesubmit', views.codesubmit, name='codesubmit'),
    url(r'^resendcode', views.resendcode, name='resendcode'),
    url(r'^addmusic', views.addmusic, name='addmusic'),
    url(r'^allmusics', views.allmusics, name='allmusics'),
    url(r'^likemusic',views.likemusic,  name='likemusic'),
    url(r'^unlikemusic',views.unlikemusic,  name='unlikemusic'),
    url(r'^profileupdate', views.profile_update, name='profile_update'),
    url(r'^reglocation', views.reglocation, name='reglocation'),
    url(r'^delmusic', views.delmusic, name='delmusic'),
    url(r'^resetpassword', views.resetpassword, name='resetpassword'),
    url(r'^rstpwd', views.rstpwd, name='rstpwd'),
]

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns=format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
