#!/usr/bin/env python3
"""
Drug Detective: Main Pipeline Orchestrator
This script orchestrates the entire pipeline for extracting drug information from scientific PDFs.
"""

import os
import json
import logging
from datetime import datetime

from pdf_extractor import extract_text_from_pdfs
from database_manager import DatabaseManager
from llm_processor import process_text_with_llm
from json_validator import validate_and_clean_json

# Configure logging
os.makedirs("./logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='./logs/drug_detective.log'
)
logger = logging.getLogger('drug_detective')

# Configuration
PDF_FOLDER = "./data/pdf_abstracts"
PROCESSED_LOG = "./data/processed_pdfs.json"
LOG_FILE = "./logs/drug_detective.log"
DB_FOLDER = "./database"
DB_PATH = os.path.join(DB_FOLDER, "drug_detective.db")


def load_processed_files():
    """Load the list of already processed PDF files."""
    try:
        if os.path.exists(PROCESSED_LOG):
            with open(PROCESSED_LOG, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Error loading processed files: {e}")
        return []


def save_processed_files(processed):
    """Save the updated list of processed PDF files."""
    try:
        with open(PROCESSED_LOG, 'w') as f:
            json.dump(processed, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving processed files: {e}")


def main():
    """Main function to run the drug detection pipeline."""
    logger.info("Starting Drug Detective pipeline")
    
    # Create folders if they don't exist
    os.makedirs(PDF_FOLDER, exist_ok=True)
    os.makedirs(DB_FOLDER, exist_ok=True)
    
    # Initialize database
    db = DatabaseManager(DB_PATH)
    db.initialize_database()
    
    # Get list of already processed files
    processed_files = load_processed_files()
    
    # Extract text from new PDFs
    pdf_data = extract_text_from_pdfs(PDF_FOLDER, processed_files)
    
    if not pdf_data:
        logger.info("No new PDFs to process")
        return
    
    # Track newly processed files
    newly_processed = []
    
    # Process each PDF
    for pdf_file, text in pdf_data:
        try:
            logger.info(f"Processing {pdf_file}")
            
            # Store abstract in database
            abstract_id = db.insert_abstract(pdf_file, text)
            
            # Process with LLM
            llm_response = process_text_with_llm(text)
            
            # Validate and clean JSON
            valid_json = validate_and_clean_json(llm_response)
            
            if not valid_json:
                logger.error(f"Invalid JSON response for {pdf_file}")
                continue
            
            # Store drug information in database
            for drug in valid_json.get('drugs', []):
                drug_name = drug.get('drug_name')
                if not drug_name:
                    continue
                
                # Insert drug and get its ID
                drug_id = db.insert_drug(drug_name, abstract_id)
                
                # Insert drug attributes
                for attr in drug.get('attributes', []):
                    attr_name = attr.get('attribute_name')
                    attr_value = attr.get('attribute_value')
                    if attr_name and attr_value:
                        db.insert_attribute(drug_id, attr_name, attr_value)
            
            # Mark file as processed
            newly_processed.append(pdf_file)
            logger.info(f"Successfully processed {pdf_file}")
            
        except Exception as e:
            logger.error(f"Error processing {pdf_file}: {e}")
    
    # Update processed files list
    processed_files.extend(newly_processed)
    save_processed_files(processed_files)
    
    logger.info(f"Pipeline complete. Processed {len(newly_processed)} new PDFs.")


if __name__ == "__main__":
    main()
