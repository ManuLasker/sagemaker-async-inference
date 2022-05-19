from typing import Optional
from pathlib import Path
from src.callbacks import validate_file_callback

import typer
import asyncio

app = typer.Typer()

@app.command()
def call_lambda(
    lambda_name: str = typer.Argument(..., help="Name of the lambda to execute asynchronously"),
    false_clients_number: int = typer.Option(..., "-n", help="Number of false clients to create"),
    lambda_event_file_path: Path = typer.Option(..., "--event-file", help="Event json file to send")
):
    pass

@app.command()
def call_sagemaker(
    sagemaker_endpoint_name: str = typer.Argument(..., help="Name of the sagemaker endpoint to execute asynchronously"),
    false_clients_number: int = typer.Option(..., "-n", help="Number of false clients to create"),
    image_file_path: Path = typer.Option(..., "--image-file", help="Image input file to send", callback=validate_file_callback)
):
    pass

if __name__ == "__main__":
    # run app
    app()