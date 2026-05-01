"""Ticket classification module."""
import json
from typing import Dict, Any


def classify_ticket(ticket: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Classify a support ticket into a category.
    
    Args:
        ticket: Ticket data with 'id', 'subject', 'body'
        config: Configuration dict with classifier settings
        
    Returns:
        Category label as string
    """
    # Simple keyword-based classification
    subject = ticket.get('subject', '').lower()
    body = ticket.get('body', '').lower()
    text = f"{subject} {body}"
    
    categories = config.get('categories', {})
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword.lower() in text:
                return category
    
    return 'general'
