from pydantic import BaseModel, Field
from typing import Annotated, List
from utils.helpers import datetime_func


class FILE_INFO(BaseModel):
    """
    Schema for metadata and extracted content of a single file.
    """
    file_name: str          # Original file name with extension
    file_title: str         # File name without extension
    file_type: str          # File extension (e.g., pdf, docx)
    file_content: str       # Extracted text content
    uploaded_at: Annotated[str, Field(default_factory=datetime_func)]  
    size_mb: int | float    # File size in MB


class FILES(BaseModel):
    """
    Schema for grouping multiple files under a user ID.
    Useful for DB storage or batch processing.
    """
    id: int                        # User ID or owner reference
    files: List[FILE_INFO]         # List of file objects
    combined_content: str          # Concatenated content of all files
