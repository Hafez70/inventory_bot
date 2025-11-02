"""Utility functions for the bot."""

import random
import string
import jdatetime
from datetime import datetime

def generate_code(prefix, length=6):
    """Generate a unique code with a prefix."""
    numbers = ''.join(random.choices(string.digits, k=length))
    return f"{prefix}{numbers}"

def generate_category_code():
    """Generate a unique code for categories."""
    return generate_code("CAT")

def generate_subcategory_code():
    """Generate a unique code for subcategories."""
    return generate_code("SUB")

def generate_brand_code():
    """Generate a unique code for brands."""
    return generate_code("BRD")

def generate_measure_type_code():
    """Generate a unique code for measure types."""
    return generate_code("MSR")

def generate_item_code():
    """Generate a unique code for items."""
    return generate_code("ITM")

def get_shamsi_date():
    """Get current Shamsi (Jalali) date."""
    return jdatetime.datetime.now().strftime("%Y/%m/%d")

def get_shamsi_datetime():
    """Get current Shamsi (Jalali) date and time."""
    return jdatetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def format_shamsi_date(date_string):
    """Format a date string to Shamsi."""
    return date_string  # Already in Shamsi format from database

def chunk_list(lst, size):
    """Split a list into chunks of specified size."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

