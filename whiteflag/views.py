from django.shortcuts import get_object_or_404, redirect, render
from .forms import WhiteFlagForm
from .models import WhiteFlag
from django.contrib.auth.decorators import login_required

CAPACITY = 80

@login_required
def white_flag(request):
    if request.method == 'POST':
        form = WhiteFlagForm(request.POST)
        if form.is_valid():
            record = form.save()
            return redirect('white_flag_edit', pk=record.pk)
    else:
        form = WhiteFlagForm()

    return render(request, 'whiteflag/white_flag.html', {
        'form': form,
        'capacity': CAPACITY,
        'record': None,
    })


@login_required
def white_flag_edit(request, pk):
    record = get_object_or_404(WhiteFlag, pk=pk)

    if request.method == 'POST':
        form = WhiteFlagForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save()
            return redirect('white_flag_edit', pk=record.pk)
    else:
        form = WhiteFlagForm(instance=record)

    return render(request, 'whiteflag/white_flag.html', {
        'form': form,
        'capacity': CAPACITY,
        'record': record,
    })