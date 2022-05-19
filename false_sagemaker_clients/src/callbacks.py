from pathlib import Path
from click.exceptions import FileError
import typer

def validate_file_callback(value: Path):
    if not value.exists():
        raise FileError(value, hint=f'the file, {value}, does not exist')
    return value