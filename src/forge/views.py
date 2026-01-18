# ghostforge/src/forge/views.py
# 
# API and Frontend Views
# 
# <diogopinto> 2025+

import os
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import AttackScenario, DefenseAnalysis
from .serializers import AttackScenarioSerializer, DefenseAnalysisSerializer
from .ai import generate_attack_content, analyze_risk_from_file
from .forms import AttackForm, DefenseForm

class AttackScenarioViewSet(viewsets.ModelViewSet):
    queryset = AttackScenario.objects.all().order_by('-created_at')
    serializer_class = AttackScenarioSerializer
    def perform_create(self, serializer):
        prompt = serializer.validated_data.get('prompt')
        target_info = serializer.validated_data.get('target_info')
        generated_content = generate_attack_content(prompt, target_info)
        serializer.save(generated_content=generated_content)

class DefenseAnalysisViewSet(viewsets.ModelViewSet):
    queryset = DefenseAnalysis.objects.all().order_by('-analyzed_at')
    serializer_class = DefenseAnalysisSerializer
    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.input_file:
            instance.file_name = os.path.basename(instance.input_file.name)
            text, score, report, level = analyze_risk_from_file(instance.input_file.path)
            instance.content_extracted = text
            instance.risk_score = score
            instance.analysis_report = report
            instance.risk_level = level
            instance.save()

# --- Frontend Views ---
def home(request):
    return render(request, 'forge/home.html')

def attack_view(request):
    result = None
    if request.method == 'POST':
        form = AttackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.generated_content = generate_attack_content(instance.prompt, instance.target_info)
            instance.save()
            result = instance
    else:
        form = AttackForm()
    
    history = AttackScenario.objects.all().order_by('-created_at')[:5]
    return render(request, 'forge/attack.html', {'form': form, 'result': result, 'history': history})

def defense_view(request):
    result = None
    if request.method == 'POST':
        form = DefenseForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            
            # EN: Only add to history if there's a file
            if instance.input_file:
                instance.file_name = request.FILES['input_file'].name
                instance.save()

                # EN: Run the AI
                text, score, report, level = analyze_risk_from_file(instance.input_file.path)
                instance.content_extracted = text
                instance.risk_score = score
                instance.analysis_report = report
                instance.risk_level = level
                instance.save()
                
                result = instance
            else:
                # #EN: No file
                pass

    else:
        form = DefenseForm()

    history = DefenseAnalysis.objects.exclude(file_name__isnull=True).exclude(file_name='').order_by('-analyzed_at')[:5]
    
    return render(request, 'forge/defense.html', {'form': form, 'result': result, 'history': history})