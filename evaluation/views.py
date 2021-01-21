from django.shortcuts import render,HttpResponseRedirect,reverse,redirect,get_object_or_404
from .forms import EvaluationQForm,BaseProsFormset,BaseConsFormset
from .models import EvaluationQModel,ProsModel,ConsModel
from django.forms import modelformset_factory
from django.views.generic import ListView,DetailView
from django.contrib import messages
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template

# creating a evaluation form
def create_eval_form(request):
    if request.method == 'POST':
        form = EvaluationQForm(request.POST)
        if form.is_valid():
            form.save()
            eval = form.save()
            #return redirect('eval_list')
            return HttpResponseRedirect(reverse('eval_detail',args=(eval.pk,)))
    else:
        form = EvaluationQForm()
    return render(request, 'create_evaluation_form.html', {'form': form})

#this is the generic class 'evaluation list' view
class EvalListView(ListView):
    model = EvaluationQModel
    template_name = 'eval_list.html'
    context_object_name = 'evals'
    ordering = ['question']
    paginate_by = 1

#this is the generic class 'topic detail' view
class EvalDetailView(DetailView):
    model = EvaluationQModel
    template_name = 'eval_detail.html'
    context_object_name = 'eval'

#this is the general evaluation search function.
def search_eval(request):
    query = request.GET.get('q')
    template = 'search_eval.html'
    start_flag = 0
    if query:
        query_pros = ProsModel.objects.filter(evaluation__question__contains=query)
        query_cons = ConsModel.objects.filter(evaluation__question__contains=query)
        if query_pros or query_cons:
            eval_name = EvaluationQModel.objects.get(question__icontains=query)
            context = {'pros':query_pros,'cons':query_cons,'eval_name':eval_name}
            return render(request, template, context)
        else:
            start_flag=1
            return render(request, template, {'start_flag': start_flag})

    return render(request,template,{'start_flag':start_flag})


def more_pros_cons(request,question_id):
    eval_name = EvaluationQModel.objects.get(pk=question_id)
    ProsFormSet = modelformset_factory(ProsModel, fields=('pros',), formset=BaseProsFormset)
    ConsFormSet = modelformset_factory(ConsModel, fields=('cons',),formset=BaseConsFormset)
    if request.method == 'POST':
        formset_pros = ProsFormSet(request.POST, queryset=ProsModel.objects.filter(evaluation__id=eval_name.id))
        formset_cons = ConsFormSet(request.POST, queryset=ConsModel.objects.filter(evaluation__id=eval_name.id))
        if formset_cons.is_valid() or formset_pros.is_valid():
            instances_cons = formset_cons.save(commit=False)
            instances_pros = formset_pros.save(commit=False)
            if instances_cons:
                for instance_con in instances_cons:
                    instance_con.evaluation_id = eval_name.id
                    instance_con.save()
            elif instances_pros:
                for instance_pro in instances_pros:
                    instance_pro.evaluation_id = eval_name.id
                    instance_pro.save()
        else:
            messages.info(request, 'Cons or Pros with the same content already exits')
            return HttpResponseRedirect(reverse('more_pros_cons', args=(eval_name.id,)))
    formset_cons = ConsFormSet(queryset=ConsModel.objects.filter(evaluation__id=eval_name.id))
    formset_pros = ProsFormSet(queryset=ProsModel.objects.filter(evaluation__id=eval_name.id))
    context = {'formset_cons': formset_cons,'formset_pros':formset_pros, 'eval_name':eval_name}
    return render(request,'more_pros_cons.html',context)


def eval_pros_cons_render_pdf(request,*args,**kwargs):
    pk = kwargs.get('pk')
    evaluation = get_object_or_404(EvaluationQModel,pk=pk)
    template_path = 'render_pdf_eval.html'
    context = {'evaluation': evaluation}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if we want to download
    # response['Content-Disposition'] = 'attachment; filename="topic_idea_details.pdf"'
    # if we want just to display
    response['Content-Disposition'] = 'filename="eval_pros_cons_details.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

