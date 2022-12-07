# Convert all HTML exports to PDF exports and create one combined report
# Requires that export_notebooks2html.sh was run successfully

# One optional parameter possible, to choose mode:
# 1: Only generate 1a and 1b
# 2: Only generate 2a and 2b
# 3: Generate 1a+1b and 2a+2b and 3a
# 4: Generate 1a+1b and 2a+2b and 3a+3b (default)
# Example: sh convert_htmls2pdf.sh 3

if [[ -z $1 ]];
then 
    mode=4 # if run without parameter, choose mode 4
else
    mode=$1
fi

# Title page
playwright pdf exports/html/titlepage.html exports/pdf/titlepage.pdf --wait-for-timeout=100

if [ $mode == 1 ] || [ $mode == 3 ] || [ $mode == 4 ]; 
then
	# OSM notebooks
	playwright pdf exports/html/1a.html exports/pdf/1a.pdf --wait-for-timeout=1000
	playwright pdf exports/html/1b.html exports/pdf/1b.pdf --wait-for-timeout=1000
fi

if [ $mode == 2 ] || [ $mode == 3 ] || [ $mode == 4 ]; 
then
	# REFERENCE notebooks
	playwright pdf exports/html/2a.html exports/pdf/2a.pdf --wait-for-timeout=1000
	playwright pdf exports/html/2b.html exports/pdf/2b.pdf --wait-for-timeout=1000
fi


# COMPARE notebooks
if [ $mode == 3 ] || [ $mode == 4 ]; 
then
	playwright pdf exports/html/3a.html exports/pdf/3a.pdf --wait-for-timeout=1000

fi

if [ $mode == 4 ]; 
then
	playwright pdf exports/html/3b.html exports/pdf/3b.pdf --wait-for-timeout=1000
fi


# Stitch together
if [ $mode == 1 ]; 
then
	gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=exports/pdf/report.pdf exports/pdf/titlepage.pdf exports/pdf/1a.pdf
fi

if [ $mode == 2 ]; 
then
gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=exports/pdf/report.pdf exports/pdf/titlepage.pdf exports/pdf/2a.pdf exports/pdf/2b.pdf
fi

if [ $mode == 3 ]; 
then
gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=exports/pdf/report.pdf exports/pdf/titlepage.pdf exports/pdf/1a.pdf exports/pdf/1b.pdf exports/pdf/2a.pdf exports/pdf/2b.pdf exports/pdf/3a.pdf
fi

if [ $mode == 4 ]; 
then
gs -q -dNOPAUSE -dBATCH -dPDFSETTINGS=/prepress -sDEVICE=pdfwrite -sOutputFile=exports/pdf/report.pdf exports/pdf/titlepage.pdf exports/pdf/1a.pdf exports/pdf/1b.pdf exports/pdf/2a.pdf exports/pdf/2b.pdf exports/pdf/3a.pdf exports/pdf/3b.pdf
fi
