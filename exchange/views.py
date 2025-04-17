from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad, ExchangeProposal
from .forms import AdForm, ExchangeProposalForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator


def ad_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    ads = Ad.objects.all()

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category__iexact=category)
    if condition:
        ads = ads.filter(condition__iexact=condition)

    paginator = Paginator(ads, 5)  # 5 объявлений на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'exchange/ad_list.html', {
        'page_obj': page_obj,
        'ads': page_obj.object_list
    })


@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('exchange:ad_list')
    else:
        form = AdForm()
    return render(request, 'exchange/ad_form.html', {'form': form})


@login_required
def ad_edit(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return redirect('exchange:ad_list')
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('exchange:ad_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'exchange/ad_form.html', {'form': form})


@login_required
def ad_delete(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user == request.user:
        ad.delete()
    return redirect('exchange:ad_list')


@login_required
def proposal_create(request):
    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exchange:proposal_list')
    else:
        form = ExchangeProposalForm()
    return render(request, 'exchange/proposal_form.html', {'form': form})


@login_required
def proposal_list(request):
    status_filter = request.GET.get('status')
    proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user)
    )
    if status_filter in ['pending', 'accepted', 'declined']:
        proposals = proposals.filter(status=status_filter)

    return render(request, 'exchange/proposal_list.html', {
        'proposals': proposals,
        'status_filter': status_filter
    })


@login_required
@require_POST
def proposal_update(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if proposal.ad_receiver.user != request.user:
        return redirect('exchange:proposal_list')

    new_status = request.POST.get('status')
    if new_status in ['accepted', 'declined']:
        proposal.status = new_status
        proposal.save()

    return redirect('exchange:proposal_list')
