from django.shortcuts import render, redirect
from .models import Entry
from .forms import EntryForm
from .FER import emotion_analysis
from .tests import send_err

#emotion_analysis('templates/1.jpg')

# Create your views here.
def index(request):
    entries = Entry.objects.order_by('-date_posted')

    context = {'entries': entries}
    
    return render(request, 'entries/index.html', context)

def add(request):
    
    if request.method == 'POST':
        
        form = EntryForm(request.POST, request.FILES)
        print("This is request.POST",request.POST, "and", request.FILES)
        print(type(request.FILES['cover']))


        # check is the data entered is valid  
        if form.is_valid():
            form.save()
            #print("This is the input image :=", form.instance.cover)
            try:
                form.instance.result = emotion_analysis(form.instance.cover)
            except:
                form.instance.result = send_err()
            form.save()


            return redirect('home')
    else:
        form = EntryForm()

    context = {'form': form }
    

    return render(request, 'entries/add.html', context) 