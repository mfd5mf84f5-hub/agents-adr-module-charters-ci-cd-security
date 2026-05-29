"""Structured JSON logging for schema architect.

Provides JSON-formatted logging with PII masking and centralized aggregation support.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional
import re


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for centralized aggregation (ELK, Datadog, etc)."""
    
    # PII patterns to mask
    PII_PATTERNS = {
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'token': r'(?:Bearer|Token)\s+[\w\-\.]+',
        'api_key': r'(?:api[_-]?key|apikey)\s*[:=]\s*[\w\-\.]+',
    }
    
    def __init__(self, service_name: str = 'schema-architect'):
        super().__init__()
        self.service_name = service_name
    
    @staticmethod
    def mask_pii(text: str) -> str:
        """Mask personally identifiable information in text."""
        if not isinstance(text, str):
            return text
        
        masked = text
        for pattern_name, pattern in JSONFormatter.PII_PATTERNS.items():
            masked = re.sub(pattern, f'[MASKED_{pattern_name.upper()}]', masked, flags=re.IGNORECASE)
        return masked
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'service': self.service_name,
            'logger': record.name,
            'message': self.mask_pii(record.getMessage()),
        }
        
        # Add context from record
        if hasattr(record, 'request_id'):
            log_data['request_id'] = record.request_id
        if hasattr(record, 'user_id'):
            log_data['user_id'] = record.user_id
        if hasattr(record, 'action'):
            log_data['action'] = record.action
        if hasattr(record, 'resource'):
            log_data['resource'] = record.resource
        if hasattr(record, 'duration_ms'):
            log_data['duration_ms'] = record.duration_ms
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Mask any PII in extra fields
        for key, value in record.__dict__.items():
            if key not in ('name', 'msg', 'args', 'created', 'filename', 'funcName',
                          'levelname', 'levelno', 'lineno', 'module', 'msecs',
                          'message', 'pathname', 'process', 'processName',
                          'relativeCreated', 'thread', 'threadName', 'exc_info',
                          'exc_text', 'stack_info', 'getMessage', 'request_id',
                          'user_id', 'action', 'resource', 'duration_ms'):
                if isinstance(value, str):
                    log_data[key] = self.mask_pii(value)
        
        return json.dumps(log_data, default=str)


def configure_json_logging(service_name: str = 'schema-architect', level: str = 'INFO'):
    """Configure JSON logging for the application.
    
    Args:
        service_name: Service identifier for logs
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level))
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add stdout handler with JSON formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(service_name=service_name))
    logger.addHandler(handler)
    
    return logger


def get_logger(name: str) -> logging.LoggerAdapter:
    """Get a logger with context helper.
    
    Usage:
        logger = get_logger(__name__)
        logger.info('Schema validated', extra={
            'request_id': '123',
            'action': 'schema_validate',
            'resource': 'schema_1',
            'duration_ms': 45
        })
    """
    return logging.getLogger(name)
