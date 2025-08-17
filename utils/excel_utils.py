# utils/excel_utils.py
"""
Helpers for exporting analysis to Excel (disk or bytes for browser downloads).
"""

from __future__ import annotations
from io import BytesIO
from typing import Dict
import pandas as pd


def save_single_df(path: str, df: pd.DataFrame, sheet_name: str = "Sheet1") -> str:
    """Save a single DataFrame to an .xlsx file on disk."""
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    return path


def save_multiple_sheets(path: str, sheets: Dict[str, pd.DataFrame]) -> str:
    """
    Save multiple DataFrames to separate sheets.
    sheets = {"Cashflow": df1, "Wealth": df2, ...}
    """
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=(name or "Sheet")[:31], index=False)
    return path


def writer_func_for_bytes(sheets: Dict[str, pd.DataFrame]):
    """
    Returns a function suitable for dash.dcc.send_bytes that writes the Excel to a buffer.
    Usage in Dash:
        from dash import dcc
        from utils.excel_utils import writer_func_for_bytes
        return dcc.send_bytes(writer_func_for_bytes({"Projection": df}), "projection.xlsx")
    """
    def _writer(b: BytesIO):
        with pd.ExcelWriter(b, engine="openpyxl") as writer:
            for name, df in sheets.items():
                df.to_excel(writer, sheet_name=(name or "Sheet")[:31], index=False)
    return _writer


def to_bytes(sheets: Dict[str, pd.DataFrame]) -> bytes:
    """Return raw Excel bytes (useful for saving to storage services)."""
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=(name or "Sheet")[:31], index=False)
    bio.seek(0)
    return bio.read()
