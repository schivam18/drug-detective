#!/usr/bin/env python3
"""
LLM Processor Module
Handles integration with language models for text processing.
"""

import os
import logging
import openai
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger('drug_detective.llm_processor')

# Get API key from environment variable
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


def build_prompt(text):
    """
    Build a prompt for the language model.
    
    Args:
        text (str): The abstract text to analyze
        
    Returns:
        str: Formatted prompt
    """
    prompt = """
The following abstract was extracted from a scientific article:

Categories and attributes to extract:
• General: Cancer Type, Generic Name, Combined With, Mechanism of Action, Line of Treatment, Trial Name, Development Stage US
• Efficacy: Primary Endpoint, Objective Response Rate (ORR), Progression-Free Survival (PFS), Hazard Ratio (HR) PFS, Complete Response (CR), Difference in PFS, Duration of Response (DOR) Rate
• Safety: Incidence of Treatment-Emergent Adverse Events Leading to Death, Thrombocytopenia, Neutropenia, Diarrhea, Constipation, Cough, Pyrexia
• Timelines: First Results Announced, Study Start Date, Study Completion Date, US Filing Date, EU Filing Date, China Filing Date, US Approval Date

Abstract Text:
"""
    prompt += text
    
    prompt += """

Respond ONLY with a JSON object in the following format:
{
     "drugs":[
          {
               "drug_name":"[Drug Name]",
               "attributes":[
                    {
                         "attribute_name":"[Attribute Name]",
                         "attribute_value":"[Value]"
                    },
                    ...
               ]
          },
          ...
     ]
}

"""
    return prompt


def process_text_with_llm(text):
    """
    Process text using a language model.
    
    Args:
        text (str): Text to process
        
    Returns:
        str: The language model's response
    """
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        return None
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Build the prompt
        prompt = build_prompt(text)
        
        # Log prompt length for debugging
        logger.info(f"Sending prompt to LLM (length: {len(prompt)} characters)")
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a scientific assistant extracting drug information from abstracts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,  # Use deterministic output for consistency
            max_tokens=2000
        )
        
        # Extract and return response content
        content = response.choices[0].message.content
        logger.info(f"Received response from LLM (length: {len(content)} characters)")
        return content
        
    except Exception as e:
        logger.error(f"Error calling language model: {e}")
        return None
