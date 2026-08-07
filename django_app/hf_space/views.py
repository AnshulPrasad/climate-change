from django.shortcuts import render
from .models import Item
from .forms import ClimateDataConfigForm
from .services import fetch_climate_data

# Create your views here.
def dashboard(request):
    # Retrieve current active source tab (defaults to 'home')
    active_source = request.GET.get('source','home')
    results = None
    form = ClimateDataConfigForm(initial={'source':active_source})

    if request.method == 'POST':
        form = ClimateDataConfigForm(request.POST)
        if form.is_valid():
            results = fetch_climate_data(form.cleaned_data)
            active_source = form.cleaned_data['source']

    context = {
        'form': form,
        'active_source': active_source,
        'results': results,
    }
    return render(request, 'core/dashboard.html', context)