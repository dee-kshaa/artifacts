"""Response generation module."""
from typing import Dict, Any, List
import json


def generate_response(ticket: Dict[str, Any], retrieved_docs: List[Dict[str, Any]], config: Dict[str, Any]) -> str:
    """
    Generate a grounded response based on retrieved documents.
    
    Args:
        ticket: Support ticket data
        retrieved_docs: List of retrieved relevant documents
        config: Configuration dict
        
    Returns:
        Generated response text
    """
    if not retrieved_docs:
        return "I apologize, but I could not find relevant documentation to address your inquiry. Please contact support directly."
    
    # Build response from top document
    top_doc = retrieved_docs[0]
    content = top_doc.get('content', top_doc.get('text', 'No content available'))
    title = top_doc.get('title', 'Documentation')
    
    response = f"""Thank you for contacting us.

Based on your inquiry, here's relevant information from our documentation:

**{title}**

{content}

If this doesn't fully address your issue, please provide more details and we'll be happy to assist further.

Best regards,
Support Team"""
    
    return response
