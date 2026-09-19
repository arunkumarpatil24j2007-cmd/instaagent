"""
Adapter package for external distribution operating systems (Leno OS, multi-agent frameworks).
"""

from .leno_adapter import LenoOSAdapter, leno_adapter, run_for_leno_os

__all__ = ["LenoOSAdapter", "leno_adapter", "run_for_leno_os"]
