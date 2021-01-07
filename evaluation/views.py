from django.shortcuts import render,HttpResponseRedirect,reverse,redirect
from .forms import EvaluationQForm,BaseProsFormset,BaseConsFormset
from .models import EvaluationQModel,ProsModel,ConsModel
from django.forms import modelformset_factory
from django.views.generic import ListView,DetailView
from django.contrib import messages

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

#this is the generic class 'topic detail' view
class EvalDetailView(DetailView):
    model = EvaluationQModel
    template_name = 'eval_detail.html'
    context_object_name = 'eval'

def more_pros_formset(request,question_id):
    eval_name = EvaluationQModel.objects.get(pk=question_id)
    ProsFormSet = modelformset_factory(ProsModel, fields=('pros',),formset=BaseProsFormset)
    if request.method == 'POST':
        formset_pros = ProsFormSet(request.POST, queryset=ProsModel.objects.filter(evaluation__id=eval_name.id))
        if formset_pros.is_valid():
            instances = formset_pros.save(commit=False)
            for instance in instances:
                instance.evaluation_id = eval_name.id
                instance.save()
        else:
            messages.info(request, 'Pros with the same content already exits')
            return HttpResponseRedirect(reverse('more_pros', args=(eval_name.id,)))
    formset_pros = ProsFormSet(queryset=ProsModel.objects.filter(evaluation__id=eval_name.id))
    context = {'formset_pros': formset_pros, 'eval_name': eval_name}
    return render(request,'more_pros.html',context)

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
            messages.info(request, 'Cons & Pros with the same content already exits')
            return HttpResponseRedirect(reverse('more_pros_cons', args=(eval_name.id,)))
    formset_cons = ConsFormSet(queryset=ConsModel.objects.filter(evaluation__id=eval_name.id))
    formset_pros = ProsFormSet(queryset=ProsModel.objects.filter(evaluation__id=eval_name.id))
    context = {'formset_cons': formset_cons,'formset_pros':formset_pros, 'eval_name':eval_name}
    return render(request,'more_pros_cons.html',context)

