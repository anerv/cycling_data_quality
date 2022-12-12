# Export all notebooks as HTML without code cells included

# One optional parameter possible, to choose mode:
# 1: Only generate 1a and 1b
# 2: Only generate 2a and 2b
# 3: Generate 1a+1b and 2a+2b and 3a
# 4: Generate 1a+1b and 2a+2b and 3a+3b (default)
# Example: python export_notebooks2html.py 3

from traitlets.config import Config
import nbformat as nbf
from nbconvert.preprocessors import TagRemovePreprocessor
from nbconvert.exporters import HTMLExporter
from nbconvert.exporters.templateexporter import default_filters
import sys, os
import subprocess

os.chdir("scripts/settings/")
exec(open("yaml_variables.py").read())
os.chdir("../../")
ipath = "scripts/"
opath = "exports/"+study_area+"/html/"

mode = 4
if sys.argv[1:]:   # test if there are atleast 1 argument (beyond [0])
    mode = int(sys.argv[1])

# Configure
c = Config()
c.TagRemovePreprocessor.remove_cell_tags = ("noex",)
c.TagRemovePreprocessor.remove_input_tags = ('remove_input',)
c.TagRemovePreprocessor.enabled = True
c.TemplateExporter.exclude_input_prompt = True
c.TemplateExporter.exclude_input = True
c.TemplateExporter.exclude_output_prompt = True
c.HTMLExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

def export_to_html(notebook_file, html_file):
    """ Export nb to html with exporter
    """

    def custom_clean_html(element):
        """ Turn clean_html into a noop, to fix svg export bug.
        Inspired by: https://github.com/jupyter/nbconvert/issues/1894#issuecomment-1334355109
        """
        return element.decode() if isinstance(element, bytes) else str(element)

    default_filters["clean_html"] = custom_clean_html
    exporter = HTMLExporter(config=c)
    exporter.register_preprocessor(TagRemovePreprocessor(config=c),True)

    print("Exporting "+notebook_file+" to "+html_file+"..")
    output, _ = exporter.from_filename(notebook_file)
    open(html_file, mode="w", encoding="utf-8").write(output)

# Convert
# OSM htmls
if mode == 1 or mode == 3 or mode == 4:
    export_to_html(ipath+"OSM/1a_initialize_osm.ipynb", opath+"1a.html")
    export_to_html(ipath+"OSM/1b_intrinsic_analysis_osm.ipynb", opath+"1b.html")

# REFERENCE htmls
if mode == 2 or mode == 3 or mode == 4:
    export_to_html(ipath+"REFERENCE/2a_initialize_reference.ipynb", opath+"2a.html")
    export_to_html(ipath+"REFERENCE/2b_intrinsic_analysis_reference.ipynb", opath+"2b.html")

# COMPARE htmls
if mode == 3 or mode == 4:
    export_to_html(ipath+"COMPARE/3a_extrinsic_analysis_metrics.ipynb", opath+"3a.html")
if mode == 4:
    export_to_html(ipath+"COMPARE/3b_extrinsic_analysis_feature_matching.ipynb", opath+"3b.html")

print("Setting up title page and post-processing HTML..")
subprocess.run(["sh","templates/postprocess_html.sh",str(mode)])
print("Done!")