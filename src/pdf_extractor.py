#!/usr/bin/env python3
"""
PDF Text Extraction Module
Extracts text from PDF files in a specified directory.
"""

import os
import logging
import PyPDF2

logger = logging.getLogger('drug_detective.pdf_extractor')


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a single PDF file.
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
        return text
    except Exception as e:
        logger.error(f"Error extracting text from {pdf_path}: {e}")
        return ""


def extract_text_from_pdfs(folder_path, processed_files):
    """
    Scan a folder for new PDF files and extract text from them.
    
    Args:
        folder_path (str): Path to the folder containing PDF files
        processed_files (list): List of already processed PDF files
        
    Returns:
        list: List of tuples containing (pdf_file, extracted_text)
    """
    results = []
    
    try:
        # Check if folder exists
        if not os.path.exists(folder_path):
            logger.warning(f"PDF folder {folder_path} does not exist")
            return results
        
        # Get all PDF files in the folder
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        
        # Filter for new files
        new_files = [f for f in pdf_files if f not in processed_files]
        
        if not new_files:
            logger.info("No new PDF files found")
            return results
        
        logger.info(f"Found {len(new_files)} new PDF files to process")
        
        # Process each new file
        for pdf_file in new_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            text = extract_text_from_pdf(pdf_path)
            
            if text:
                results.append((pdf_file, text))
                logger.info(f"Successfully extracted text from {pdf_file}")
            else:
                logger.warning(f"Failed to extract text from {pdf_file}")
        
        return results
    
    except Exception as e:
        logger.error(f"Error in extract_text_from_pdfs: {e}")
        return results
