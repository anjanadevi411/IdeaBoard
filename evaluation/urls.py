from django.urls import path
from .views import (create_eval_form,EvalListView,more_pros_cons,EvalDetailView,eval_pros_cons_render_pdf,
                    search_eval)

urlpatterns = [
    path('evallist/', EvalListView.as_view(), name='eval_list'),
    path('evalform/', create_eval_form, name='eval_form'),
    path('evaldetail/<int:pk>',EvalDetailView.as_view(),name='eval_detail'),
    path('pros_cons/<int:question_id>/',more_pros_cons,name='more_pros_cons'),
    path('pdf_format/<int:pk>',eval_pros_cons_render_pdf,name='pdf_format_eval'),
    path('search_eval/',search_eval,name='search_eval'),
]