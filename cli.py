import typer
from pathlib import Path

import format_huffman as fmth

app = typer.Typer(help="Custom compressor (LZ77 + Huffman)")


def _default_compress_out(input_path: Path) -> Path:
    return input_path.with_suffix(".bart")


def _default_decompress_out(input_path: Path) -> Path:
    
    if input_path.suffix == ".bart":
        return input_path.with_suffix("")
    
  
    return input_path.with_suffix(input_path.suffix)


@app.command()
def compress(
    input: Path,
    output: Path | None = typer.Option(None, "-o", "--output"),
):
    """
    Compress file using LZ77 + Huffman.
    """
    if not input.exists():
        typer.echo(f"Input file does not exist: {input}", err=True)
        raise typer.Exit(code=2)

    out_path = output or _default_compress_out(input)

    try:
        fmth.compress_file(str(input), str(out_path))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Created: {out_path}")


@app.command()
def decompress(
    input: Path,
    output: Path | None = typer.Option(None, "-o", "--output"),
):
    """
    Decompress file produced by this compressor.
    """
    if not input.exists():
        typer.echo(f"Input file does not exist: {input}", err=True)
        raise typer.Exit(code=2)

    out_path = output or _default_decompress_out(input)

    try:
        fmth.decompress_file(str(input), str(out_path))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Created: {out_path}")


if __name__ == "__main__":
    app()