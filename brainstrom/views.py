from django.shortcuts import render,redirect,HttpResponseRedirect,reverse,get_object_or_404
from django.views.generic import CreateView,ListView,DetailView
from .models import TopicModel,IdeaModel
from .forms import TopicForm,IdeaForm,BaseIdeaFormset
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from .filters import IdeaFilter
import enchant
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages

'''class TopicCreateView(CreateView):
    model = TopicModel
    template_name = 'topic_create.html'
    fields = '__all__'
    success_url = reverse_lazy('topic_list')'''

# in this function creating a topic and checking whether it is meaningful word or not. If valid
# creating a topic or else redirecting to another page where they can go to again to topic creation page
'''def create_topic_form(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            d = enchant.Dict('en_US')
            check1 = d.check(topic.topicname.split()[0])
            if check1:
                topic = form.save()
                return HttpResponseRedirect(reverse('topic_detail',args=(topic.pk,)))
            else:
                return HttpResponseRedirect(reverse_lazy('enter_meaning'))
                #return HttpResponse('Please enter meaning full words')
            #return redirect('topic_list')
    else:
        form = TopicForm()
    return render(request, 'create_topic_form.html', {'form': form})'''

# creating a topic and redirecting to detail page when it is a valid topic
def create_topic_form(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save()
            return HttpResponseRedirect(reverse('topic_detail',args=(topic.pk,)))
            #return redirect('topic_list')
    else:
        form = TopicForm()
    return render(request, 'create_topic_form.html', {'form': form})

#this is the generic class 'topic list' view
class TopicListView(ListView):
    model = TopicModel
    template_name = 'topic_list1.html'
    context_object_name = 'topics'
    ordering = ['topicname']
    paginate_by = 2

#testing
#this is the generic class 'topic list' view
class TopicListViewNew(ListView):
    model = TopicModel
    template_name = 'topic_list.html'
    context_object_name = 'topics'
    ordering = ['topicname']
    #paginate_by = 2

#this is the generic class 'topic detail' view
class TopicDetailView(DetailView):
    model = TopicModel
    template_name = 'topic_detail.html'
    context_object_name = 'topic'

'''class IdeaCreateView(CreateView):
    model = IdeaModel
    template_name = 'idea_create.html'
    fields = '__all__'
    success_url = reverse_lazy('idea_list')'''

# in this function creating a idea and checking whether it is meaningful word or not. If valid
# creating a idea or else redirecting to same idea form creation page.
def create_idea_form(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save()
            topic = TopicModel.objects.get(topicname = idea.topicname_idea)
            return HttpResponseRedirect(reverse('topic_detail', args=(topic.pk,)))
            #return redirect('idea_list')
    else:
        form = IdeaForm()
    return render(request, 'idea_create.html', {'form': form})

#this is the generic class 'idea list' view
class IdeaListView(ListView):
    model = IdeaModel
    template_name = 'idea_list.html'
    context_object_name = 'ideas'
    ordering = ['idea']

    #this is the method for filtering/search the topics which are there in the database
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = IdeaFilter(self.request.GET,queryset=self.get_queryset())
        return context


#this is the generic class 'idea detail' view
class IdeaDetailView(DetailView):
    model = IdeaModel
    template_name = 'idea_detail.html'
    context_object_name = 'idea'

'''def search1(request):
    word = enchant.Dict()
    query = request.GET.get('q')
    #topic_words = TopicModel.objects.filter(topicname=query)
    if word.check(query.capitalize()):
        print(query)
        query_set = IdeaModel.objects.all()
        if query:
            query_set = query_set.filter(topicname_idea__topicname__icontains=query)
            context = {'ideas':query_set,'query':query,}
    else:
        context = {'query':query}
    template = 'search.html'
    return render(request,template,context)'''

#this is the general topic search function.
#presently not in use
def search(request):
    query = request.GET.get('q')
    template = 'search.html'
    if query:
        query_set = IdeaModel.objects.filter(topicname_idea__topicname__icontains=query)
        context = {'ideas':query_set,'query':query}
        return render(request, template, context)
    return render(request,template)

#this is the function for redirecting users to create more ideas using modelformsets.
#and also checking wheather users are creating meaning full ideas or not.Done through enchant.
#Displays the same form with warning if users do not enter meaning full words
'''def more_ideas_formset(request,topicname_id):
    flag = 0
    topicname = TopicModel.objects.get(pk=topicname_id)
    IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',),formset=BaseIdeaFormset)
    IdeaFormSet(queryset=IdeaModel.objects.none())
    if request.method == 'POST':
        formset = IdeaFormSet(request.POST, queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                d = enchant.Dict('en_US')
                check_word = d.check(instance.idea.split()[0])
                if check_word:
                    instance.topicname_idea_id = topicname.id
                    instance.save()
                else:
                    flag = 1
                    formset = IdeaFormSet(queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
                    context = {'formset': formset, 'topicname': topicname,'flag':flag}
                    return render(request, 'more_ideas.html', context)
                    #return HttpResponseRedirect(reverse_lazy('enter_meaning'))
    formset = IdeaFormSet(queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
    context = {'formset': formset, 'topicname': topicname,'flag':flag}
    return render(request,'more_ideas.html',context)'''

'''def more_ideas_formset(request,topicname_id):
    topicname = TopicModel.objects.get(pk=topicname_id)
    IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',),)
    if request.method == 'POST':
        formset = IdeaFormSet(request.POST, queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.topicname_idea_id = topicname.id
                instance.save()
        #else:
         #   messages.info(request, 'Idea with the same content already exits')
          #  return redirect('topic_list')
    formset = IdeaFormSet(queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
    context = {'formset': formset, 'topicname': topicname}
    return render(request,'more_ideas.html',context)'''

def more_ideas_formset(request,topicname_id):
    topicname = TopicModel.objects.get(pk=topicname_id)
    IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',),formset=BaseIdeaFormset)
    if request.method == 'POST':
        formset = IdeaFormSet(request.POST, queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.topicname_idea_id = topicname.id
                instance.save()
        else:
            messages.info(request, 'Idea with the same content already exits')
            return HttpResponseRedirect(reverse('more_ideas', args=(topicname.id,)))
    formset = IdeaFormSet(queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
    context = {'formset': formset, 'topicname': topicname}
    return render(request,'more_ideas.html',context)

#test_sticky_notes
def more_ideas(request,topicname_id):
    topicname = TopicModel.objects.get(pk=topicname_id)
    IdeaFormSet = modelformset_factory(IdeaModel, fields=('idea',),formset=BaseIdeaFormset)
    if request.method == 'POST':
        formset = IdeaFormSet(request.POST, queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.topicname_idea_id = topicname.id
                instance.save()
        else:
            messages.info(request, 'Idea with the same content already exits')
            return HttpResponseRedirect(reverse('create_form', args=(topicname.id,)))
    formset = IdeaFormSet(queryset=IdeaModel.objects.filter(topicname_idea__id=topicname.id))
    context = {'formset': formset, 'topicname': topicname}
    return render(request,'create_form.html',context)


def topic_idea_render_pdf(request,*args,**kwargs):
    pk = kwargs.get('pk')
    topic = get_object_or_404(TopicModel,pk=pk)
    template_path = 'render_pdf_topic.html'
    context = {'topic': topic}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # if we want to download
    # response['Content-Disposition'] = 'attachment; filename="topic_idea_details.pdf"'
    # if we want just to display
    response['Content-Disposition'] = 'filename="topic_idea_details.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response







