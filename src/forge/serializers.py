# ghostforge/src/forge/serializers.py
# 
# Serializers to convert the model to JSON for the API.
# 
# <diogopinto> 2025+

from rest_framework import serializers
from .models import AttackScenario, DefenseAnalysis

# EN: Some fields are set to read only because they won't have any user input

# -----------------------------------------------------------------
# EN: Serializer for the AttackScenario model.
class AttackScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttackScenario
        fields = '__all__'
        read_only_fields = ['generated_content', 'created_at']



# -----------------------------------------------------------------
# EN: Serializer for the DefenseAnalysis model.
class DefenseAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefenseAnalysis
        fields = '__all__'
        read_only_fields = ['risk_score', 'risk_level', 'analysis_report', 'analyzed_at']