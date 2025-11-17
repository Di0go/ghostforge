# ghostforge/src/forge/views.py
# 
# API Views that handle the logic for Attack and Defense endpoints
# Create, read, update and delete (CRUD)
# 
# <diogopinto> 2025+

from rest_framework import viewsets
from .models import AttackScenario, DefenseAnalysis
from .serializers import AttackScenarioSerializer, DefenseAnalysisSerializer
from .ai import generate_attack_content, analyze_risk_from_file



# -----------------------------------------------------------------
# EN: ViewSet for handling Attack Scenarios.
class AttackScenarioViewSet(viewsets.ModelViewSet):
    queryset = AttackScenario.objects.all().order_by('-created_at')
    serializer_class = AttackScenarioSerializer

    # --------------------------------------------------------------------------------------
    # EN: perform_create() is a method in the viewsets that handles the creation of new objects
    def perform_create(self, serializer):
        # EN: Get the user prompt and the target information from the newly serialized data
        prompt = serializer.validated_data.get('prompt')
        target_info = serializer.validated_data.get('target_info')
        
        # EN: Call the langchain attack orchestrator function from ai.py
        generated_content = generate_attack_content(prompt, target_info)
        
        # EN: Save to DB
        serializer.save(generated_content=generated_content)



# -----------------------------------------------------------------
# EN: ViewSet for handling Defense Analysis.
class DefenseAnalysisViewSet(viewsets.ModelViewSet):
    queryset = DefenseAnalysis.objects.all().order_by('-analyzed_at')
    serializer_class = DefenseAnalysisSerializer

    def perform_create(self, serializer):
        # EN: Save the uploaded file so docling has a valid path to read from
        instance = serializer.save()
        
        if instance.input_file:
            file_path = instance.input_file.path
            
            # EN: Call the langchain defense orchestrator function from ai.py
            text, score, report, level = analyze_risk_from_file(file_path)
            
            # EN: Save to DB
            instance.content_extracted = text
            instance.risk_score = score
            instance.analysis_report = report
            instance.risk_level = level
            instance.save()