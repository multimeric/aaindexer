project = 'aaindexer'
copyright = '2022, Michael Milton'
author = 'Michael Milton'
release = '0.1.0'
extensions = [
    'sphinxcontrib.restbuilder',
    'sphinx.ext.autodoc',
    'sphinx_click'
]
autodoc_typehints = "description"
autodoc_class_signature = "separated"
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.rst']
html_theme = 'alabaster'
html_static_path = ['_static']
