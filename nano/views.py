from django.shortcuts import render
from django.views import generic
from .models import *
from .QC import start as qc_start
from .GroupComparison import start as gc_start
import os

# Create your views here.

def upload_files(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        if pk:
            input_file = InputFile.objects.get(id=pk)
            input_file.status = 'DONE'
            input_file.save()
            qc = QC()
            qc.input_file = input_file
            pdf_files, quality_control = qc_start(qc)
            qc_files = []
            for fi in pdf_files:
                qc_file = QCFiles()
                qc_file.upload_file = fi
                qc_file.save()
                os.rename(fi, qc_file.upload_file.path)
                qc_files.append(qc_file)
            qc.save()
            qc.quality_control = quality_control
            qc.qc_files.set(qc_files)
            qc.save()
            os.rename(quality_control, qc.quality_control.path)
        else:
            slug = request.POST.get('slug')
            files = request.FILES.getlist('csv_files')
            upload_files = []
            for f in files:
                file_model=Files(upload_file=f)
                file_model.save()
                upload_files.append(file_model)
            input_file = InputFile()
            input_file.slug = slug
            input_file.save()
            input_file.files.set(upload_files)
            input_file.save()
    context = {'input_files': InputFile.objects.filter()}
    return render(request, 'list_upload_files.html', context)

def index(request):
    return render(request, 'index.html')

def qc(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        gene = request.POST.get('gene')
        if pk:
            qc = QC.objects.get(id=pk) 
            files = gc_start(qc, gene)
            gc = GroupComparison()
            gc.qc = qc
            gc_files = []
            for fi in files:
                gc_file = GCFiles()
                gc_file.upload_file = fi
                gc_file.save()
                fi = os.path.join(os.getcwd(), fi)
                os.rename(fi, gc_file.upload_file.path)
                gc_files.append(gc_file)
            qc.status = 'DONE'
            qc.save()
            gc.save()
            gc.gc_files.set(gc_files)
            gc.save()
    context = {'qcs': QC.objects.filter(status='NEW')}
    return render(request, 'list_qc_files.html', context)

def group_comparison(request):
    pass

def ge_volcano(request):
    pass

