#!/usr/bin/env python3
"""Generate an offline QR code as an inline SVG data-URI.

Dev-time tool only. Vercel never runs this (scripts/ is in .vercelignore);
the generated data-URI is committed directly into the HTML so the deployed
site stays zero-build and has no external dependency (no api.qrserver.com,
no Google Charts, etc.).

Usage:
    python3 scripts/gen-qr.py "https://testflight.apple.com/join/XXXX"

Prints a `data:image/svg+xml;base64,...` string to stdout. Paste it into the
relevant <img src="..."> in index.html. Re-run with the real App Store URL
once the app ships, then re-paste.

Self-bootstraps its one dependency (segno) into scripts/.venv on first run.
"""

import base64
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
VENV = os.path.join(HERE, ".venv")
VENV_PY = os.path.join(VENV, "bin", "python")


def _bootstrap():
    """Ensure we are running inside scripts/.venv with segno installed."""
    if os.path.abspath(sys.executable) != os.path.abspath(VENV_PY):
        if not os.path.exists(VENV_PY):
            subprocess.check_call([sys.executable, "-m", "venv", VENV])
        os.execv(VENV_PY, [VENV_PY, os.path.abspath(__file__), *sys.argv[1:]])

    try:
        import segno  # noqa: F401
    except ImportError:
        subprocess.check_call([VENV_PY, "-m", "pip", "install", "--quiet", "segno"])


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python3 scripts/gen-qr.py <url>")

    _bootstrap()
    import segno

    url = sys.argv[1]
    qr = segno.make(url, error="m")

    buf = io.BytesIO()
    qr.save(
        buf,
        kind="svg",
        scale=8,
        border=2,
        dark="#111827",   # gray-900, matches the dark store badges
        light="#ffffff",  # solid white quiet zone for reliable scanning
        xmldecl=False,
        svgns=True,
    )
    data_uri = "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
    print(data_uri)


if __name__ == "__main__":
    main()
