# bart_zip

Custom LZ77 + Huffman file compressor with a simple Flask frontend.

This project implements:

- LZ77 algorithm
- Huffman algorithm
- Custom binary format `.bart`
- Basic web upload form for compression and decompression

## Run locally

    pip install -r requirements.txt
    flask --app app run

Open:

    http://127.0.0.1:5000

## Command line

Compress a file:

    python cli.py compress file.txt

Decompress a file:

    python cli.py decompress file.bart

## Render deployment

This project includes `render.yaml`.

On Render, create a new Blueprint from the repository or create a Web Service
manually with:

    Build Command: pip install -r requirements.txt
    Start Command: gunicorn app:app
