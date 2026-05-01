"""Safety check module for inappropriate content."""
from typing import Dict, Any


def check_safety(content: str, request_type: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Check if ticket contains inappropriate or harmful content.
    
    Args:
        content: Request text to check
        request_type: Type of request
        config: Configuration dict with safety settings
        
    Returns:
        Dictionary with risk_level, reason, and is_safe
    """
    if config is None:
        config = {
            'high_risk_keywords': [
                'fraud', 'unauthorized', 'stolen', 'hack', 'hacked',
                'chargeback', 'lawsuit', 'legal', 'privacy breach',
                'compromised', 'identity theft', 'exploit', 'malware'
            ]
        }
    
    text = content.lower()
    high_risk_keywords = config.get('high_risk_keywords', [])
    
    # Check for high-risk content
    for keyword in high_risk_keywords:
        if keyword.lower() in text:
            return {
                'risk_level': 'high',
                'reason': f'High-risk content detected: {keyword}',
                'is_safe': False
            }
    
    # Check for suspicious patterns
    if 'delete' in text and 'system' in text and 'code' in text.lower():
        return {
            'risk_level': 'high',
            'reason': 'Suspicious request pattern detected',
            'is_safe': False
        }
    
    # Default to safe
    return {
        'risk_level': 'low',
        'reason': 'Content appears safe',
        'is_safe': True
    }


def should_escalate(safety_check: Dict[str, Any]) -> bool:
    """
    Determine if ticket should be escalated based on safety check.
    
    Args:
        safety_check: Result from check_safety function
        
    Returns:
        True if should escalate, False otherwise
    """
    return safety_check.get('risk_level') == 'high' or not safety_check.get('is_safe', True)
