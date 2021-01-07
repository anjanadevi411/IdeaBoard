from django.urls import path
from .views import create_eval_form,EvalListView,more_pros_formset,more_pros_cons,EvalDetailView

urlpatterns = [
    path('evallist/', EvalListView.as_view(), name='eval_list'),
    path('evalform/', create_eval_form, name='eval_form'),
    path('evaldetail/<int:pk>',EvalDetailView.as_view(),name='eval_detail'),
    path('pros/<int:question_id>/',more_pros_formset,name='more_pros'),
    path('cons/<int:question_id>/',more_pros_cons,name='more_pros_cons'),
    ]