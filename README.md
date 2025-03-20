# Drug Detective: Uncovering Drug Secrets from Scientific PDFs

A modular pipeline for extracting structured drug information from scientific PDF abstracts.

## Project Overview

Drug Detective automatically scans scientific PDF abstracts, extracts text, identifies drug information, and stores the structured data in a database for easy retrieval and analysis.

## Features

- PDF text extraction from a designated folder
- SQLite database for storing extracted data
- LLM integration for intelligent information extraction
- JSON validation and cleaning
- Detailed logging for debugging
- Modular design for maintainability and extensibility

## Setup Instructions

### Prerequisites

- Python 3.7+
- Virtual environment (recommended)

### Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   source venv/bin/activate 
   # On macOS/Linux 

   venv\Scripts\activate
   # On Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up your OpenAI API key:
   ```
   export OPENAI_API_KEY=your_api_key_here
   # On macOS/Linux

   set OPENAI_API_KEY=your_api_key_here
   # On Windows
   ```

## Usage

1. Place PDF abstracts in the `pdf_abstracts` folder
2. Run the pipeline:
   ```
   python main.py
   ```
3. Check the console output and log file for processing results

## Project Structure

- `main.py`: Main pipeline orchestrator
- `pdf_extractor.py`: Handles PDF text extraction
- `database_manager.py`: Manages database operations
- `llm_processor.py`: Integrates with language model API
- `json_validator.py`: Validates and cleans LLM responses
- `processed_pdfs.json`: Keeps track of processed files
- `drug_detective.log`: Detailed log of all operations
- `drug_detective.db`: SQLite database with extracted information

## Database Schema

- **abstracts**: Stores the extracted text from PDFs
  - id (PRIMARY KEY)
  - filename
  - text
  - processed_date

- **drugs**: Stores drug information
  - id (PRIMARY KEY)
  - name
  - abstract_id (FOREIGN KEY -> abstracts.id)

- **attributes**: Stores drug attributes
  - id (PRIMARY KEY)
  - drug_id (FOREIGN KEY -> drugs.id)
  - name
  - value

## Extracted Attributes

### General
- Cancer Type
- Generic Name
- Combined With
- Mechanism of Action
- Line of Treatment
- Trial Name
- Development Stage US

### Efficacy
- Primary Endpoint
- Objective Response Rate (ORR)
- Progression-Free Survival (PFS)
- Hazard Ratio (HR) PFS
- Complete Response (CR)
- Difference in PFS
- Duration of Response (DOR) Rate

### Safety
- Incidence of Treatment-Emergent Adverse Events Leading to Death
- Thrombocytopenia
- Neutropenia
- Diarrhea
- Constipation
- Cough
- Pyrexia

### Timelines
- First Results Announced
- Study Start Date
- Study Completion Date
- US Filing Date
- EU Filing Date
- China Filing Date
- US Approval Date

## Extending the Project

To add new features:
1. Add new attribute categories in the LLM prompt
2. Extend the database schema if needed
3. Add additional post-processing functions
