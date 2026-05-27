from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from agents.models import ResearchProject
from agents.services.runner import run_product_research


def home(request):
    return render(request, 'index.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def product_research(request):
    if request.method == 'POST':
        asin  = request.POST.get('asin', '').strip()
        niche = request.POST.get('niche', '').strip()
        file  = request.FILES.get('helium_file')

        if asin and niche:
            project = ResearchProject.objects.create(
                asin=asin,
                niche=niche,
                uploaded_file=file,
            )
            try:
                run_product_research(project)
            except Exception:
                pass
            return redirect('iTrendAI:product_research_overview', pk=project.pk)

    qs = ResearchProject.objects.all()
    paginator = Paginator(qs, 10)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'productresearch.html', {'projects': page, 'paginator': paginator})


def product_research_overview(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk)
    return render(request, 'productresearch_overview.html', {'project': project})


def edit_project(request, pk):
    if request.method != 'POST':
        return redirect('iTrendAI:product_research')

    project = get_object_or_404(ResearchProject, pk=pk)
    asin  = request.POST.get('asin', '').strip()
    niche = request.POST.get('niche', '').strip()
    new_file = request.FILES.get('helium_file')

    if asin:
        project.asin = asin[:20]
    if niche:
        project.niche = niche
    if new_file:
        project.uploaded_file = new_file
        project.result = None
        project.error_message = ''
        project.status = 'pending'

    project.save()
    project.refresh_from_db()

    if new_file:
        try:
            run_product_research(project)
        except Exception:
            pass
        return redirect('iTrendAI:product_research_overview', pk=project.pk)

    return redirect('iTrendAI:product_research')


def delete_project(request, pk):
    if request.method != 'POST':
        return redirect('iTrendAI:product_research')

    project = get_object_or_404(ResearchProject, pk=pk)
    project.delete()
    return redirect('iTrendAI:product_research')
