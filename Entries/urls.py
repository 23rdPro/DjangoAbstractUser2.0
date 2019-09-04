
# from django.conf.urls import url, include
from django.urls import include, re_path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth import login
from django.contrib.auth.views import logout, login


from django.views.generic import TemplateView

from entryApp.views import (
    admin_function, 
    record_detail, 
    # GeneratePDF, 
    super_admin_list,
    html_to_csv_view, 
    html_to_pdf_view,
    delete_record,
    update_record,
    welcome_page,
    # home_page_home
)


urlpatterns = [
    # re_path('admin/', admin.site.urls),
    re_path(r'^$', welcome_page, name='welcome'),
    re_path(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    re_path(r'^login/$', login, name='login'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^register/', include(('entryApp.urls', 'entryApp'), namespace='entry')),
    re_path(r'^record/', admin_function, name='list'),
    re_path(r'^super-admin/', super_admin_list, name='super'),
    re_path(r'^(delete/(?P<id>\d+))/$', delete_record, name='delete'),
    re_path(r'^(entry/(?P<id>\d+))/$', record_detail, name='detail'),
    re_path(r'^(edit/(?P<id>\d+))/$', update_record, name='edit'),
    # re_path('downloads/', GeneratePDF.as_view(), name='pdf'),
    re_path('html_to_pdf_view/', html_to_pdf_view, name='html_to_pdf_view'),
    re_path('html_to_csv_view/', html_to_csv_view, name='html_to_csv_view'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)