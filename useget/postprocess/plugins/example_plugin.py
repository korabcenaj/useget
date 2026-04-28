"""
Example post-processing plugin.
"""

def process(file_path: str, config: dict) -> None:
    """
    Example plugin that logs the file processed.
    """
    import logging
    logging.info(f"[Plugin] Processed file: {file_path}")
