# ghostforge/src/forge/ai.py
# 
# The brain behind the web-app!
# 
# <diogopinto> 2025+

import re
import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# EN: PyPDFLoader for now instead of docling (due to performance issues)
from langchain_community.document_loaders import PyPDFLoader 

LLM_URL = "http://ghostforge-llm:11434"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "tinyllama")

def get_llm():
    return ChatOllama(
        base_url=LLM_URL,
        model=MODEL_NAME,
        temperature=0.2,
        num_ctx=4096 
    )

# -----------------------------------------------------------------
def generate_attack_content(prompt_text, target_info=None):
    llm = get_llm()
    
    system_msg = (
        "You are a social engineering expert. Generate a realistic attack text."
        "\n\n"
        "FORMAT RULES:\n"
        "1. Use Markdown headers like '### Subject' or '### Message'.\n"
        "2. Do not include placeholders like '[Insert Name]'. Invent realistic details.\n"
        "3. Keep it direct and convincing."
    )
    
    user_msg = f"Task: Generate a social engineering attack for: {prompt_text}"
    if target_info:
        user_msg += f"\nTarget Info: {target_info}"

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("user", user_msg),
    ])
    
    try:
        chain = prompt_template | llm | StrOutputParser()
        return chain.invoke({})
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------------------------------------------
def analyze_risk_from_file(file_path):
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        extracted_text = "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return (f"Error reading PDF: {str(e)}", 0, "Extraction Failed", "LOW")

    llm = get_llm()
    
    system_msg = (
        "You are a cybersecurity analyst. Detect phishing or malicious intent."
        "\n\n"
        "RESPONSE FORMAT:\n"
        "Line 1: SCORE: <risk_number_0_to_100>\n"
        "Line 2: REPORT: <write a short analysis summary here>\n"
        "\n"
        "RULES:\n"
        "- If safe, score is low (0-30).\n"
        "- If suspicious (urgency, money, links), score is high (70-100).\n"
        "- Do not use brackets like [ ]. Just write the text."
    )
    
    # EN: Limit text size to fit in 2048 context window 
    safe_text = extracted_text[:2000]

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("user", f"Analyze this text:\n\n{safe_text}"),
    ])
    
    try:
        chain = prompt_template | llm | StrOutputParser()
        result = chain.invoke({})
        
        # --- Parsing ---
        score = 0
        score_match = re.search(r"SCORE:\s*(\d+)", result, re.IGNORECASE)
        if score_match:
            score = int(score_match.group(1))
        
        report = re.sub(r"SCORE:\s*\d+", "", result, flags=re.IGNORECASE)
        report = re.sub(r"REPORT:", "", report, flags=re.IGNORECASE).strip()
        
        if len(report) < 5: report = result

        level = 'LOW'
        if score >= 85: level = 'CRITICAL'
        elif score >= 60: level = 'HIGH'
        elif score >= 35: level = 'MEDIUM'

        return (extracted_text, score, report, level)

    except Exception as e:
        return (extracted_text, 0, f"Error: {str(e)}", "LOW")