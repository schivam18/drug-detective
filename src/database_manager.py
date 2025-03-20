#!/usr/bin/env python3
"""
Database Manager Module
Handles all database operations for the Drug Detective pipeline.
"""

import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger('drug_detective.database')


class DatabaseManager:
    """
    Database manager class for drug detective operations.
    """
    
    def __init__(self, db_path):
        """
        Initialize database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def initialize_database(self):
        """Create database tables if they don't exist."""
        try:
            # Create Abstracts table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS abstracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                text TEXT NOT NULL,
                processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create Drugs table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS drugs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                abstract_id INTEGER,
                FOREIGN KEY (abstract_id) REFERENCES abstracts (id)
            )
            ''')
            
            # Create Attributes table
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attributes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drug_id INTEGER,
                name TEXT NOT NULL,
                value TEXT NOT NULL,
                FOREIGN KEY (drug_id) REFERENCES drugs (id)
            )
            ''')
            
            self.conn.commit()
            logger.info("Database tables initialized")
        except sqlite3.Error as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def insert_abstract(self, filename, text):
        """
        Insert an abstract into the database.
        
        Args:
            filename (str): The PDF filename
            text (str): The extracted text
            
        Returns:
            int: ID of the inserted abstract
        """
        try:
            self.cursor.execute(
                "INSERT INTO abstracts (filename, text) VALUES (?, ?)",
                (filename, text)
            )
            self.conn.commit()
            abstract_id = self.cursor.lastrowid
            logger.info(f"Inserted abstract ID {abstract_id} for {filename}")
            return abstract_id
        except sqlite3.Error as e:
            logger.error(f"Error inserting abstract: {e}")
            self.conn.rollback()
            raise
    
    def insert_drug(self, name, abstract_id):
        """
        Insert a drug into the database.
        
        Args:
            name (str): The drug name
            abstract_id (int): The abstract ID
            
        Returns:
            int: ID of the inserted drug
        """
        try:
            self.cursor.execute(
                "INSERT INTO drugs (name, abstract_id) VALUES (?, ?)",
                (name, abstract_id)
            )
            self.conn.commit()
            drug_id = self.cursor.lastrowid
            logger.info(f"Inserted drug ID {drug_id} for {name}")
            return drug_id
        except sqlite3.Error as e:
            logger.error(f"Error inserting drug: {e}")
            self.conn.rollback()
            raise
    
    def insert_attribute(self, drug_id, name, value):
        """
        Insert a drug attribute into the database.
        
        Args:
            drug_id (int): The drug ID
            name (str): The attribute name
            value (str): The attribute value
        """
        try:
            self.cursor.execute(
                "INSERT INTO attributes (drug_id, name, value) VALUES (?, ?, ?)",
                (drug_id, name, value)
            )
            self.conn.commit()
            logger.debug(f"Inserted attribute {name}={value} for drug ID {drug_id}")
        except sqlite3.Error as e:
            logger.error(f"Error inserting attribute: {e}")
            self.conn.rollback()
            raise
    
    def get_drugs_by_abstract(self, abstract_id):
        """
        Get all drugs associated with an abstract.
        
        Args:
            abstract_id (int): The abstract ID
            
        Returns:
            list: List of drug dictionaries
        """
        try:
            self.cursor.execute(
                "SELECT id, name FROM drugs WHERE abstract_id = ?",
                (abstract_id,)
            )
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error getting drugs by abstract: {e}")
            raise
    
    def get_attributes_by_drug(self, drug_id):
        """
        Get all attributes for a drug.
        
        Args:
            drug_id (int): The drug ID
            
        Returns:
            list: List of attribute dictionaries
        """
        try:
            self.cursor.execute(
                "SELECT name, value FROM attributes WHERE drug_id = ?",
                (drug_id,)
            )
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Error getting attributes by drug: {e}")
            raise
