from django.urls import path, include
from api.apps.account.views import auth
from api.apps.account.views.account import (
	in_account,
	out_account,
)

app_name = 'account'

urlpatterns = [
	path('registration/', auth.RegistrationView.as_view(), name='registration'),
	path('activate/<slug:uid>/<slug:token>/', auth.ActivateView.as_view(), name='activate'),

	path('reset/passwd/', auth.ResetPasswdMailView.as_view(), name='reset_passwd'),
	path('change/passwd/', auth.NewPasswdView.as_view(), name='change_passwd'),
	path('confirm/passwd/<slug:uid>/<slug:token>/', auth.ConfirmNewPasswdView.as_view(), name='confirm_passwd'),

	path('logout/', auth.LogoutView.as_view(), name='logout'),
	path('out/', include([
		path('list/', out_account.ListView.as_view(), name='out_accounts'),
		path('item/<int:pk>/', out_account.ItemView.as_view(), name='out_account'),
	])),
]
urlpatterns += [
	path('in/', include([
		path('list/', in_account.ListView.as_view(), name='in_accounts'),
		path('item/<int:pk>/', in_account.ItemView.as_view(), name='in_account'),
		path('create/', in_account.CreateView.as_view(), name='in_account_create'),
		path('edit/<int:pk>/', in_account.EditView.as_view(), name='in_account_edit'),
		path('delete/<int:pk>/', in_account.DeleteView.as_view(), name='in_account_delete'),
	]))
]