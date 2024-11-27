from mpi4py import MPI
from PIL import Image, ImageFilter
import numpy as np
import os
import argparse

"""
MPI Sharpen Image Processing
Run:
    mpiexec -np 4 python mpi_sharpen.py --input=input_image.png --output=sharpened_image.png

Parameters:
    --input: Path to the input image
    --output: Path to save the sharpened image
"""

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Sharpen an image using MPI.")
parser.add_argument("--input", type=str, required=True, help="Path to input image")
parser.add_argument("--output", type=str, required=True, help="Path to save sharpened image")
args = parser.parse_args()

input_image_path = args.input
output_image_path = args.output

if rank == 0:
    # Root process: Read the image and divide it into chunks
    if not os.path.exists(input_image_path):
        raise FileNotFoundError(f"Input file {input_image_path} does not exist.")

    image = Image.open(input_image_path)
    image_array = np.array(image)

    # Split the image array into chunks along the height
    chunks = np.array_split(image_array, size, axis=0)
else:
    # Non-root processes: Initialize empty chunk
    chunks = None

# Scatter chunks to all processes
chunk = comm.scatter(chunks, root=0)

# Each process applies a sharpening filter to its chunk
# Convert chunk to PIL Image for filtering
chunk_image = Image.fromarray(chunk)
sharpened_chunk_image = chunk_image.filter(ImageFilter.SHARPEN)

# Convert back to numpy array for gathering
sharpened_chunk = np.array(sharpened_chunk_image)

# Gather sharpened chunks back to the root process
sharpened_chunks = comm.gather(sharpened_chunk, root=0)

if rank == 0:
    # Root process: Reconstruct the full sharpened image
    sharpened_image = np.vstack(sharpened_chunks)
    output_image = Image.fromarray(sharpened_image)
    output_image.save(output_image_path)
    print(f"Sharpened image saved as {output_image_path}")