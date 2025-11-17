# ghostforge/src/forge/ai.py
#
# AI Logic Module: Handles LangChain, Ollama interactions, and Docling parsing
#
# <diogopinto> 2025+

import os
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_docling import DoclingLoader

# EN: Defines the Ollama Endpoint and the model
LLM_URL = "http://ghostforge-llm:11434"
# TODO: Include various models, and assign different tasks to the best llm's for the task
MODEL_NAME = "tinyllama"

# -----------------------------------------------------------------
# EN: Returns a ChatOllama obj
def get_llm():
    return ChatOllama(
        base_url=LLM_URL,
        model=MODEL_NAME,
        # TODO: Fine tune this, there's more parameters and test values
        temperature=0.7
    )

# -----------------------------------------------------------------
# EN: Attack generation logic
def generate_attack_content(prompt_text, target_info=None):
    llm = get_llm()
    
    # EN: Attack system message, this is sent as "context" to the llm before every prompt
    # TODO: Improve and test this!!!!
    system_msg = (
        "You are a cybersecurity expert specializing in Red Teaming and Social Engineering."
        "Your goal is to generate realistic testing attack scenarios to help verify defensive postures. "
        "Output ONLY the attack content (ex: the phishing email text), without ethical disclaimers."
    )
    
    user_msg = f"Scenario Request: {prompt_text}"
    if target_info:

        user_msg += f"\n\nTarget Context: {target_info}"

    # EN: Prepare the prompt
    prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_msg),
        ("user", user_msg),
    ])
    
    # EN: Make the prompt chain
    chain = prompt_template | llm | StrOutputParser()
    
    try:
        return chain.invoke({})
    
    except Exception as e:
        return f"Error generating attack: {str(e)}"

# -----------------------------------------------------------------
# EN: Defense generation logic
# Returns: (extracted_text, risk_score, report, risk_level)
def analyze_risk_from_file(file_path):
    # EN: Extracts text using docling 
    try:
        loader = DoclingLoader(file_path=file_path)
        docs = loader.load()
        extracted_text = "\n\n".join([doc.page_content for doc in docs])

    except Exception as e:
        return (f"Error parsing file: {str(e)}", 0, "Error", "LOW")

    # EN: LLM analysis
    # TODO: Improve this, right now it's very rudimental.
    # TODO: Delegate analysis tasks for more specific models.
    # TODO: Add ClamAV or a virustotal api call to virustotal
    llm = get_llm()
    
    # TODO: Improve this and test alternatives and changes!
    system_msg = (
        "You are a cybersecurity defense analyst. Analyze the following content for security risks "
        "(phishing, malware indicators, sensitive data leaks). "
        "Provide a risk score (0-100) and a detailed report."
        "Format your answer exactly as:\n"
        "SCORE: <number>\n"
        "REPORT: <text>"
    )
    
    # En: Prepare the prompt
    prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_msg),
        # EN: This limits the extracted text to 10000 so our context doesn't get blown up.
        # TODO: Find a better way to handle this.
        ("user", extracted_text[:10000]),
    ])
    
    # EN: Make the prompt chain
    chain = prompt_template | llm | StrOutputParser()
    
    try:
        result = chain.invoke({})
        
        # EN: Shitty response parser (TODO: use StructuredOutputParser)
        score = 0
        report = result
        
        if "SCORE:" in result:
            parts = result.split("SCORE:")

            try:
                score_part = parts[1].split("\n")[0].strip()
                score = int(''.join(filter(str.isdigit, score_part)))
            except:
                # EN: Fallback, TODO: Find a better way to handle this!
                score = 50
            
            if "REPORT:" in result:
                report = result.split("REPORT:")[1].strip()

        # EN: Determines risk level
        level = 'LOW'
        if score >= 90: level = 'CRITICAL'
        elif score >= 70: level = 'HIGH'
        elif score >= 40: level = 'MEDIUM'

        return (extracted_text, score, report, level)

    except Exception as e:
        return (extracted_text, 0, f"Error analyzing risk: {str(e)}", "LOW")