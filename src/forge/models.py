
# ghostforge/src/forge/models.py
# 
# Models for the forge app, they store both attack and defense information
# 
# <diogopinto> 2025+

from django.db import models



# -----------------------------------------------------------------
# EN: Stores the attack scenarios.
class AttackScenario(models.Model):
    title = models.CharField(max_length=200, help_text="Attack Title")
    prompt = models.TextField(help_text="User prompt")
    
    # TODO: Maybe make this JSON???
    target_info = models.TextField(blank=True, null=True, help_text="Target Context (RAG)")
    
    # EN: Result
    generated_content = models.TextField(blank=True, null=True, help_text="Generated Content")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



# -----------------------------------------------------------------
# EN: Stores the defense analysis 
class DefenseAnalysis(models.Model):

    RISK_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    input_file = models.FileField(upload_to='uploads/', blank=True, null=True, help_text="Document for Analysis")
    file_name = models.CharField(max_length=255, blank=True, null=True)
    # TODO: docling needs to fill this context
    content_extracted = models.TextField(blank=True, null=True)
    
    # EN: Results
    risk_score = models.IntegerField(default=0, help_text="Risk score")
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default='LOW')
    analysis_report = models.TextField(blank=True, null=True, help_text="LLM detailed report analysis")
    
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analysis {self.id} - {self.risk_level}"
