#!/usr/bin/env python3
"""
JSON Validator Module
Validates and cleans JSON responses from the language model.
"""

import json
import logging
import re

logger = logging.getLogger('drug_detective.json_validator')


def validate_and_clean_json(json_text):
    """
    Validate and clean JSON response from the language model.
    
    Args:
        json_text (str): JSON text to validate and clean
        
    Returns:
        dict: Cleaned JSON object or None if invalid
    """
    if not json_text:
        logger.error("Empty JSON text received")
        return None
    
    # First attempt: Try to parse as-is
    try:
        json_obj = json.loads(json_text)
        logger.info("JSON valid on first attempt")
        return json_obj
    except json.JSONDecodeError as e:
        logger.warning(f"Initial JSON parsing failed: {e}")
    
    # Second attempt: Clean up the JSON text
    cleaned_text = clean_json_text(json_text)
    
    try:
        json_obj = json.loads(cleaned_text)
        logger.info("JSON valid after cleaning")
        return json_obj
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing failed after cleaning: {e}")
        
        # Last attempt: Extract JSON within markdown code blocks
        try:
            # Extract JSON from markdown code blocks if present
            json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
            matches = re.findall(json_pattern, json_text)
            
            if matches:
                for match in matches:
                    try:
                        json_obj = json.loads(match)
                        logger.info("JSON extracted from code block")
                        return json_obj
                    except:
                        continue
        except Exception as e:
            logger.error(f"Failed to extract JSON from markdown: {e}")
    
    return None


def clean_json_text(json_text):
    """
    Clean and fix common JSON formatting issues.
    
    Args:
        json_text (str): JSON text to clean
        
    Returns:
        str: Cleaned JSON text
    """
    # Remove any leading/trailing text
    json_pattern = r"({[\s\S]*})"
    matches = re.search(json_pattern, json_text)
    if matches:
        json_text = matches.group(1)
    
    # Fix single quotes to double quotes
    json_text = json_text.replace("'", '"')
    
    # Fix unquoted keys
    json_text = re.sub(r'([{,])\s*([a-zA-Z0-9_]+)\s*:', r'\1"\2":', json_text)
    
    # Fix trailing commas
    json_text = re.sub(r',\s*([}\]])', r'\1', json_text)
    
    # Remove additional characters outside the JSON object
    json_text = re.sub(r'^[^{]*({[\s\S]*})[^}]*$', r'\1', json_text)
    
    logger.debug("JSON text cleaned")
    return json_text


def validate_drug_structure(json_obj):
    """
    Validate if the drug JSON structure is correct.
    
    Args:
        json_obj (dict): JSON object to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(json_obj, dict):
        logger.error("JSON is not a dictionary")
        return False
    
    if 'drugs' not in json_obj:
        logger.error("'drugs' key not found in JSON")
        return False
    
    if not isinstance(json_obj['drugs'], list):
        logger.error("'drugs' is not a list")
        return False
    
    for i, drug in enumerate(json_obj['drugs']):
        if not isinstance(drug, dict):
            logger.error(f"Drug at index {i} is not a dictionary")
            return False
        
        if 'drug_name' not in drug:
            logger.error(f"Drug at index {i} has no 'drug_name'")
            return False
        
        if 'attributes' not in drug:
            logger.error(f"Drug at index {i} has no 'attributes'")
            return False
        
        if not isinstance(drug['attributes'], list):
            logger.error(f"Drug at index {i} 'attributes' is not a list")
            return False
        
        for j, attr in enumerate(drug['attributes']):
            if not isinstance(attr, dict):
                logger.error(f"Attribute at index {j} for drug {i} is not a dictionary")
                return False
            
            if 'attribute_name' not in attr:
                logger.error(f"Attribute at index {j} for drug {i} has no 'attribute_name'")
                return False
            
            if 'attribute_value' not in attr:
                logger.error(f"Attribute at index {j} for drug {i} has no 'attribute_value'")
                return False
    
    logger.info("Drug JSON structure validation passed")
    return True
