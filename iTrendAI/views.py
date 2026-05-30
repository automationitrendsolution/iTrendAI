import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import ResearchReport

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/10a6809b-1c1f-499d-a2e1-ee2b68eca80f"


def agents(request):
    return render(request, 'agents.html')


def newproductresearch(request):
    history = ResearchReport.objects.all()
    return render(request, 'newproductresearch.html', {'history': history})


def newproductresearchreport(request):
    if request.method != 'POST':
        return redirect('iTrendAI:newproductresearch')

    product_name  = request.POST.get('product_name', '').strip()
    category      = request.POST.get('category', '').strip()
    uploaded_file = request.FILES.get('file')
    file_name     = uploaded_file.name if uploaded_file else '—'

    form_data = {'product_name': product_name, 'category': category}
    files = {}
    if uploaded_file:
        files['file'] = (uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

    try:
        if files:
            resp = requests.post(N8N_WEBHOOK_URL, data=form_data, files=files, timeout=600)
        else:
            resp = requests.post(N8N_WEBHOOK_URL, json=form_data, timeout=600)
        resp.raise_for_status()

        try:
            payload = resp.json()
            if isinstance(payload, list) and payload:
                payload = payload[0]
            if isinstance(payload, dict):
                ai_output = (
                    payload.get('output')
                    or payload.get('text')
                    or payload.get('message')
                    or payload.get('result')
                    or payload.get('report')
                    or json.dumps(payload, indent=2)
                )
            else:
                ai_output = str(payload)
        except ValueError:
            ai_output = resp.text

    except requests.exceptions.ConnectionError:
        ai_output = "ERROR: Could not connect to the analysis service. Make sure n8n is running on localhost:5678."
    except requests.exceptions.Timeout:
        ai_output = "ERROR: The analysis service took too long to respond (timeout after 10 min)."
    except requests.exceptions.RequestException as e:
        ai_output = f"ERROR: {e}"

    # Save to DB only on success
    report = None
    if not ai_output.startswith('ERROR:'):
        report = ResearchReport.objects.create(
            product_name=product_name,
            category=category,
            file_name=file_name,
            ai_output=ai_output,
        )

    history = ResearchReport.objects.all()

    context = {
        'product_name': product_name,
        'category':     category,
        'file_name':    file_name,
        'ai_output':    ai_output,
        'history':      history,
        'current_id':   report.pk if report else None,
    }
    return render(request, 'newproductresearchreport.html', context)


def view_report(request, pk):
    report  = get_object_or_404(ResearchReport, pk=pk)
    history = ResearchReport.objects.all()
    context = {
        'product_name': report.product_name,
        'category':     report.category,
        'file_name':    report.file_name,
        'ai_output':    report.ai_output,
        'history':      history,
        'current_id':   report.pk,
    }
    return render(request, 'newproductresearchreport.html', context)


def delete_report(request, pk):
    if request.method == 'POST':
        report = get_object_or_404(ResearchReport, pk=pk)
        report.delete()
    return redirect('iTrendAI:newproductresearch')
