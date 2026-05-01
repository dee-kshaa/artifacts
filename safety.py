"""Safety check module for inappropriate content."""
from typing import Dict, Any, Tuple


def check_safety(ticket: Dict[str, Any], config: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Check if ticket contains inappropriate or harmful content.
    
    Args:
        ticket: Ticket data with 'id', 'subject', 'body'
        config: Configuration dict with safety settings
        
    Returns:
        Tuple of (is_safe: bool, reason: str)
    """
    unsafe_keywords = config.get('unsafe_keywords', [])
    
    subject = ticket.get('subject', '').lower()
    body = ticket.get('body', '').lower()
    text = f"{subject} {body}"
    
    for keyword in unsafe_keywords:
        if keyword.lower() in text:
            return False, f"Contains unsafe keyword: {keyword}"
    
    return True, "Safe"
