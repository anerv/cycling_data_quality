# Convert all HTML exports to PDF exports and create one report
# Requires that export_notebooks2html.sh was run successfully

# OSM notebooks
playwright pdf exports/html/1a.html exports/pdf/1a.pdf --wait-for-timeout=1000

playwright pdf exports/html/1b.html exports/pdf/1b.pdf --wait-for-timeout=1000

# REFERENCE notebooks
playwright pdf exports/html/2a.html exports/pdf/2a.pdf --wait-for-timeout=1000

playwright pdf exports/html/2b.html exports/pdf/2b.pdf --wait-for-timeout=1000

# COMPARE notebooks
playwright pdf exports/html/3.html exports/pdf/3.pdf --wait-for-timeout=1000

playwright pdf exports/html/4.html exports/pdf/4.pdf --wait-for-timeout=1000

gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=exports/pdf/report.pdf exports/pdf/1a.pdf exports/pdf/1b.pdf exports/pdf/2a.pdf exports/pdf/2b.pdf exports/pdf/3.pdf exports/pdf/4.pdf