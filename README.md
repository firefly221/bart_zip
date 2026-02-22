# bart_zip -- Custom LZ77 + Huffman file compressor

file compressor written in Python.

This project implements:

-   LZ77 algorithm
-   Huffman algorithm
-   Custom binary format (.bart)
-   Command-line interface built with Typer library

------------------------------------------------------------------------

## Usage

### Compress a file

    python cli.py compress file.txt

Output:

    file.bart

### Decompress a file

    python cli.py decompress file.bart

Output:

    file

You can specify output manually:

    python cli.py decompress file.bart -o restored.txt

------------------------------------------------------------------------

## Example Compression Results 
### EXAMPLES ARE IN examples/ FOLDER

Tested on various datasets:


   File Type              Original Size     Compressed Size
  ---------------------  --------------- -----------------
  Repeating patterns      5.6 MB          56 KB
  Mixed patterns          1.7 MB          759 KB
  Random (a/b/c only)     1.9 MB          912 KB

