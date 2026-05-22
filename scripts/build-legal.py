#!/usr/bin/env python3
"""Regenerate the legal pages (legal/privacy.html, legal/terms.html) from the
source-of-truth Markdown in the InstaPickleball app repository.

This is a MANUAL, dev-time maintenance tool — it is NOT part of the deploy.
Vercel never runs it; the site stays pure static HTML. Run it yourself
whenever docs/legal/*.md in the app repo changes, then commit the new HTML.

Usage:
    python3 scripts/build-legal.py [--src PATH_TO_docs/legal]

The default --src assumes the app repo sits next to this one:
    <parent>/InstaSportsInfoWeb       <- this repo
    <parent>/Claude_Code_APP_Prj      <- app repo (holds docs/legal/*.md)

The script self-bootstraps the one dependency it needs (python-markdown) into
scripts/.venv on first run, so the only thing you ever type is the command
above. See CLAUDE.md for the full regeneration checklist.
"""
import argparse
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_ROOT, "legal")
DEFAULT_SRC = os.path.normpath(
    os.path.join(REPO_ROOT, "..", "Claude_Code_APP_Prj", "docs", "legal")
)


def _ensure_markdown():
    """Make `import markdown` work — bootstrap a local venv if it doesn't.

    python-markdown is the only dependency. We install it into scripts/.venv
    (git-ignored) and re-exec this script inside that venv. macOS Python is
    PEP 668 "externally managed", so a venv is the clean install path."""
    try:
        import markdown  # noqa: F401

        return
    except ImportError:
        pass

    venv = os.path.join(REPO_ROOT, "scripts", ".venv")
    bindir = "Scripts" if os.name == "nt" else "bin"
    venv_py = os.path.join(venv, bindir, "python" + (".exe" if os.name == "nt" else ""))

    if not os.path.exists(venv_py):
        print("First run — setting up python-markdown in scripts/.venv ...")
        subprocess.check_call([sys.executable, "-m", "venv", venv])
        subprocess.check_call([venv_py, "-m", "pip", "install", "--quiet", "markdown"])

    # Re-exec inside the venv (which has `markdown`), preserving CLI args.
    os.execv(venv_py, [venv_py, os.path.abspath(__file__)] + sys.argv[1:])


_ensure_markdown()
import markdown  # noqa: E402  (only importable after _ensure_markdown)

HEAD = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>__TITLE__</title>
    <link rel="icon" href="/favicon.ico" sizes="any" />
    <link rel="icon" type="image/png" href="/favicon.png" />
    <link rel="apple-touch-icon" href="/favicon.png" />
    <script src="https://cdn.tailwindcss.com/3.4.16"></script>
    <script>
      tailwind.config = {
        theme: { extend: { colors: { primary: "#4CAF50", secondary: "#FF9800" } } },
      };
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css"
    />
    <style>
      body { font-family: 'Inter', sans-serif; }
      /* Legal document typography. Tailwind's CDN build ships Preflight, which
         strips default heading/list styling — restore it here so the
         Markdown-rendered content reads like a real document. The
         .legal-content class prefix keeps these rules from leaking out. */
      .legal-content { color: #374151; line-height: 1.7; }
      .legal-content h1 { font-size: 2rem; font-weight: 700; color: #111827; margin-bottom: 0.25rem; }
      .legal-content h2 { font-size: 1.5rem; font-weight: 700; color: #111827;
        margin-top: 2.5rem; margin-bottom: 1rem; padding-top: 1.75rem; border-top: 1px solid #e5e7eb; }
      .legal-content h3 { font-size: 1.15rem; font-weight: 600; color: #1f2937;
        margin-top: 1.75rem; margin-bottom: 0.6rem; }
      .legal-content p { margin: 0.9rem 0; }
      .legal-content ul, .legal-content ol { margin: 0.9rem 0; padding-left: 1.6rem; }
      .legal-content ul { list-style: disc; }
      .legal-content ol { list-style: decimal; }
      .legal-content li { margin: 0.3rem 0; }
      .legal-content a { color: #4CAF50; text-decoration: underline; }
      .legal-content strong { font-weight: 600; color: #111827; }
      /* Source Markdown uses `---` purely as section separators; the styled
         h2 top border already divides sections, so hide the bare rules. */
      .legal-content hr { display: none; }
      .legal-content blockquote { margin: 1.5rem 0; padding: 0.85rem 1.1rem;
        border-left: 4px solid #4CAF50; background: #f9fafb; font-weight: 500; }
      .legal-content blockquote p { margin: 0.2rem 0; }
      .legal-content table { width: 100%; border-collapse: collapse;
        margin: 1.5rem 0; font-size: 0.875rem; }
      .legal-content th, .legal-content td { border: 1px solid #e5e7eb;
        padding: 0.55rem 0.75rem; text-align: left; vertical-align: top; }
      .legal-content th { background: #f3f4f6; font-weight: 600; }
    </style>
  </head>
  <body class="bg-white">
    <nav class="bg-white shadow-sm sticky top-0 z-40">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <a href="/" aria-label="InstaPickleball home" class="inline-flex items-center gap-1.5 text-primary text-xl font-bold italic leading-none sm:gap-2 sm:text-2xl">
            <img src="/logo3x.png" alt="" class="h-7 w-7 shrink-0 sm:h-8 sm:w-8" />
            <span>InstaPickleball</span>
          </a>
          <div class="flex items-center space-x-3 text-sm sm:space-x-6 sm:text-base">
            <a href="/" class="text-gray-700 hover:text-primary font-medium">Home</a>
            <a href="/contact_us" class="text-gray-700 hover:text-primary font-medium">Contact Us</a>
          </div>
        </div>
      </div>
    </nav>
    <main>
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
        <article class="legal-content">
"""

TAIL = """        </article>
        <div class="mt-14 pt-8 border-t border-gray-200 text-sm text-gray-500">
          See also: __CROSSLINK__ &nbsp;·&nbsp;
          <a href="/" class="text-primary hover:underline">Back to Home</a>
        </div>
      </div>
    </main>
__FOOTER__
  </body>
</html>
"""

# Footer mirrors index.html's footer, with these deliberate differences:
#  - brand logo says InstaPickleball (the product), not the company name
#  - Terms / Privacy hrefs point at the real pages
#  - Contact Us uses a root-absolute path (legal pages live under /legal/)
#  - copyright year is current; "InstaSportsInfo, Inc." stays — legal entity
FOOTER = """    <footer class="bg-gray-900 text-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div class="mb-4 inline-flex items-center gap-2 text-primary text-2xl font-bold italic leading-none">
              <img src="/logo3x.png" alt="" class="h-8 w-8 shrink-0" />
              <span>InstaPickleball</span>
            </div>
            <p class="text-gray-400 mb-4">
              Connect with your local pickleball community and take your game to
              the next level.
            </p>
            <div class="flex space-x-4">
              <a href="#" class="text-gray-400 hover:text-white w-10 h-10 flex items-center justify-center rounded-full bg-gray-800">
                <i class="ri-facebook-fill"></i>
              </a>
              <a href="#" class="text-gray-400 hover:text-white w-10 h-10 flex items-center justify-center rounded-full bg-gray-800">
                <i class="ri-twitter-x-fill"></i>
              </a>
              <a href="#" class="text-gray-400 hover:text-white w-10 h-10 flex items-center justify-center rounded-full bg-gray-800">
                <i class="ri-instagram-fill"></i>
              </a>
              <a href="#" class="text-gray-400 hover:text-white w-10 h-10 flex items-center justify-center rounded-full bg-gray-800">
                <i class="ri-youtube-fill"></i>
              </a>
            </div>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Company</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-400 hover:text-white">About Us</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white">Careers</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white">Press</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white">Blog</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Support</h3>
            <ul class="space-y-2">
              <li><a href="#" class="text-gray-400 hover:text-white">Help Center</a></li>
              <li><a href="/contact_us" class="text-gray-400 hover:text-white">Contact Us</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white">Community Guidelines</a></li>
              <li><a href="#" class="text-gray-400 hover:text-white">FAQs</a></li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Legal</h3>
            <ul class="space-y-2">
              <li><a href="/legal/terms" class="text-gray-400 hover:text-white">Terms of Service</a></li>
              <li><a href="/legal/privacy" class="text-gray-400 hover:text-white">Privacy Policy</a></li>
            </ul>
          </div>
        </div>
        <div class="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-400 text-sm">
            &copy; 2026 InstaSportsInfo, Inc. All rights reserved.
          </p>
          <div class="flex items-center space-x-4 mt-4 md:mt-0">
            <i class="ri-visa-fill ri-lg text-gray-400"></i>
            <i class="ri-mastercard-fill ri-lg text-gray-400"></i>
            <i class="ri-paypal-fill ri-lg text-gray-400"></i>
            <i class="ri-apple-fill ri-lg text-gray-400"></i>
          </div>
        </div>
      </div>
    </footer>"""

# (md filename, output filename, <title>, crosslink HTML to the sibling doc)
PAGES = [
    (
        "privacy.md",
        "privacy.html",
        "Privacy Policy — InstaPickleball",
        '<a href="/legal/terms" class="text-primary hover:underline">Terms of Service</a>',
    ),
    (
        "terms.md",
        "terms.html",
        "Terms of Service — InstaPickleball",
        '<a href="/legal/privacy" class="text-primary hover:underline">Privacy Policy</a>',
    ),
]


def strip_frontmatter(text):
    """Remove a leading YAML frontmatter block (--- ... ---)."""
    if not text.startswith("---"):
        return text
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1:]).lstrip("\n")
    return text


def render(src_dir, md_name, out_name, title, crosslink):
    src_path = os.path.join(src_dir, md_name)
    with open(src_path, encoding="utf-8") as f:
        body_md = strip_frontmatter(f.read())
    # extra -> tables/abbr/etc; toc -> heading ids for deep links;
    # nl2br -> single newlines become <br> (address blocks, lettered lists).
    body_html = markdown.markdown(
        body_md, extensions=["extra", "toc", "nl2br"], output_format="html5"
    )
    page = (
        HEAD.replace("__TITLE__", title)
        + body_html
        + "\n"
        + TAIL.replace("__CROSSLINK__", crosslink).replace("__FOOTER__", FOOTER)
    )
    out_path = os.path.join(OUT_DIR, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    rel = os.path.relpath(out_path, REPO_ROOT)
    print(f"  {rel}  ({len(page):,} bytes)")


def main():
    parser = argparse.ArgumentParser(description="Regenerate the legal HTML pages.")
    parser.add_argument(
        "--src",
        default=DEFAULT_SRC,
        help="Path to the app repo's docs/legal directory "
        f"(default: {DEFAULT_SRC})",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.src):
        sys.exit(
            f"ERROR: source directory not found: {args.src}\n"
            "Pass the correct path with --src PATH_TO_docs/legal"
        )

    os.makedirs(OUT_DIR, exist_ok=True)
    print(f"Rendering legal pages from {args.src}")
    for md_name, out_name, title, crosslink in PAGES:
        render(args.src, md_name, out_name, title, crosslink)
    print("Done. Review the diff, then commit the updated HTML.")


if __name__ == "__main__":
    main()
