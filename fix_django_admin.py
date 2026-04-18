#!/usr/bin/env python
"""
Fix Django Admin Context Copy Error for Python 3.14 + Django 4.2
"""

import sys
from django.template.context import Context

# Monkey patch pour Python 3.14 Django compatibility
def fixed_copy(self):
    """Fixed __copy__ for Django Context in Python 3.14"""
    duplicate = Context(self.dicts[:], autoescape=self.autoescape)
    duplicate.use_l10n = self.use_l10n
    duplicate.use_tz = self.use_tz
    duplicate.template_engine = self.template_engine
    return duplicate

Context.__copy__ = fixed_copy

print("Django Admin Context Fix Applied - Restart Backend")

