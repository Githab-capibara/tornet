# Sphinx configuration for ReadTheDocs.
# Referenced by readthedocs.yaml -> sphinx.configuration.
#
# TorNet documentation is GitHub-native Markdown; MyST Parser lets Sphinx
# consume the same .md files that render on GitHub, so there is a single
# source of truth (docs/README.md is the landing page).

project = "TorNet"
author = "ByteBreach"
copyright = "2026, ByteBreach"
release = "2.0.2"

extensions = [
    "myst_parser",
]

# The landing page is docs/README.md, not the Sphinx default "index".
master_doc = "README"

# Markdown sources live in subdirectories (adr/, architecture/, ...);
# index them all without requiring per-directory toc trees.
exclude_patterns = [
    "_build",
    # templates live in every docs subdirectory and root; exclude them all
    "**/template.md",
]

# Keep GitHub-style relative links working under Sphinx.
myst_heading_anchors = 3

html_theme = "alabaster"
