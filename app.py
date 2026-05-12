from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory

from flask import Flask, render_template, request, send_file

import format_huffman as fmth


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded = request.files["file"]
        action = request.form["action"]

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_path = tmp_path / uploaded.filename
            output_path = tmp_path / ("result.bart" if action == "compress" else "result")

            uploaded.save(input_path)

            if action == "compress":
                fmth.compress_file(str(input_path), str(output_path))
            else:
                fmth.decompress_file(str(input_path), str(output_path))

            result = BytesIO(output_path.read_bytes())

        return send_file(result, as_attachment=True, download_name=output_path.name)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
