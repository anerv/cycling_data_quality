# Convert all HTML exports to PDF exports and create one combined report
# Requires that export_notebooks2html.sh was run successfully

# OSM notebooks
playwright pdf exports/html/1a.html exports/pdf/1a.pdf --wait-for-timeout=1000
playwright pdf exports/html/1b.html exports/pdf/1b.pdf --wait-for-timeout=1000

# REFERENCE notebooks
playwright pdf exports/html/2a.html exports/pdf/2a.pdf --wait-for-timeout=1000
playwright pdf exports/html/2b.html exports/pdf/2b.pdf --wait-for-timeout=1000

# COMPARE notebooks
playwright pdf exports/html/3a.html exports/pdf/3a.pdf --wait-for-timeout=1000
playwright pdf exports/html/3b.html exports/pdf/3b.pdf --wait-for-timeout=1000

# Stitch together
gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=exports/pdf/report.pdf exports/pdf/1a.pdf exports/pdf/1b.pdf exports/pdf/2a.pdf exports/pdf/2b.pdf exports/pdf/3a.pdf exports/pdf/3b.pdf