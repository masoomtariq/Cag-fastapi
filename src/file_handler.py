"""
file_handler.py
---------------
Handles incoming UploadFile objects, delegates extraction to extractors,
and returns structured Pydantic models (FILE_INFO / FILES) ready for DB storage.
"""

from fastapi import UploadFile, HTTPException
from tempfile import NamedTemporaryFile
from file_models import FILE_INFO, FILES
from utils.file_processing import extract_pdf, extract_txt, extract_docx, extract_excel, extract_image, extract_pptx, extract_epub
import logging
import colorlog

# Create a colored handler
handler = colorlog.StreamHandler()

# Set specific colors for log levels
handler.setFormatter(colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s - %(levelname)s - %(message)s",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',    # Customizes logger.info to print in green
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    }
))

logger = colorlog.getLogger("MyLogger")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Temporary directory where files are processed
files_path = 'tmp/uploads'

# Mapping of supported file types to their extractor functions
EXTRACTORS = {
    "pdf": extract_pdf,
    "txt": extract_txt,
    "docx": extract_docx,
    "pptx": extract_pptx,
    "epub": extract_epub,
    "xls": extract_excel,
    "xlsx": extract_excel,
    "csv": extract_excel,
    "jpg": extract_image,
    "jpeg": extract_image,
    "png": extract_image,
    "bmp": extract_image
}

class File_Handler:
    """
    File_Handler processes uploaded files:
    - Extracts metadata (name, type, size).
    - Extracts text content using the appropriate extractor.
    - Builds Pydantic models for DB storage.
    """

    def __init__(self, file_object: UploadFile, user_id: int):
        """
        Initialize handler with uploaded file and user ID.

        Args:
            file_object (UploadFile): The file uploaded via FastAPI.
            user_id (int): Unique ID of the user uploading the file.
        """
        self.file_object = file_object
        self.user_id = user_id
        self.file_name = file_object.filename

        # Separate file title and type (extension)
        self.file_title, self.file_type = self.file_name.rsplit('.', 1)

        # Calculate file size in MB
        file_object.file.seek(0, 2)   # Move pointer to end
        size_in_bytes = file_object.file.tell()  # Get total size
        file_object.file.seek(0)      # Reset pointer back to start
        self.size_mb = round(size_in_bytes / (1024 ** 2), 2)

        logger.info(f"File initialized: {self.file_name} (Size: {self.size_mb} MB)")

    def load_and_process(self):
        """
        Save file temporarily, extract text using appropriate extractor,
        and store the extracted content in self.file_content.

        Raises:
            HTTPException: If file type is unsupported,
                           extraction fails, or no text is returned.
        """
        with NamedTemporaryFile(
            dir=files_path,
            prefix=f'{self.user_id}_{self.file_name}_',
            suffix=f'.{self.file_type}',
            delete=False
        ) as temp_file:
            # Write uploaded file content into temporary file
            temp_file.write(self.file_object.file.read())

            logger.debug(f"Temporary file created: {temp_file.name} for user ID: {self.user_id}")
            # Select extractor based on file type (extension)
            extractor = EXTRACTORS.get(self.file_type, None)
            if extractor is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported file type: {self.file_type}"
                )

            try:
                logger.error(f"Extracting text from {self.file_type.upper()} file: {self.file_name}")
                extracted_text = extractor(temp_file.name)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error extracting text from {self.file_type.upper()} file: {str(e)}"
                )

            logger.critical(f"Extraction completed for file: {self.file_name}. Extracted text length: {len(extracted_text)} characters.")
            if extracted_text == "" or extracted_text is None:
                raise HTTPException(
                    status_code=422,
                    detail="Failed to extract text from the file."
                )

            # Store extracted content
            self.file_content = extracted_text

    def create_file_model(self):
        """
        Build a FILE_INFO model for this file.

        Returns:
            dict: Serialized FILE_INFO model.
        """
        self.file_data = FILE_INFO(
            file_name=self.file_name,
            file_title=self.file_title,
            file_type=self.file_type,
            file_content=self.file_content,
            size_mb=self.size_mb
        )
        return self.file_data.model_dump()

    def create_files_model(self):
        """
        Build a FILES model (user + multiple files).
        Currently wraps only the single uploaded file.

        Returns:
            dict: Serialized FILES model.
        """
        if not getattr(self, "file_data", None):
            self.create_file_model()

        self.files_data = FILES(
            id=self.user_id,
            files=[self.file_data],
            combined_content=self.file_content
        )
        return self.files_data.model_dump()