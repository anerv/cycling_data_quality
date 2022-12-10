# Convert all HTML exports to PDF exports and create one combined report
# Requires that export_notebooks2html.sh was run successfully

# One optional parameter possible, to choose mode:
# 1: Only generate 1a and 1b
# 2: Only generate 2a and 2b
# 3: Generate 1a+1b and 2a+2b and 3a
# 4: Generate 1a+1b and 2a+2b and 3a+3b (default)
# Example: python convert_htmls2pdf.py 3

pdfoptions = {"format": "A4",
"display_header_footer": True,
"margin": {"top": "1.1in", "bottom": "1.1in", "left": "0.6in", "right": "0.5in"},
"prefer_css_page_size": True
}

section_names = {"1a": "1a. Load OSM data",
"1b": "1b. Intrinsic OSM analysis",
"2a": "2a. Load reference data",
"2b": "2b. Intrinsic reference analysis",
"3a": "3a. Extrinsic analysis",
"3b": "3b. Feature matching"
}

import sys, os
os.chdir("scripts/settings/")
exec(open("yaml_variables.py").read())
os.chdir("../../")
ipath = "exports/"+study_area+"/html/"
opath = "exports/"+study_area+"/pdf/"

import subprocess, shlex
subprocess.run(["sh","templates/settemplates.sh"])
with open("exports/"+study_area+"/html/header_template.html") as f:
    pdfoptions["header_template"] = f.read()
with open("exports/"+study_area+"/html/footer_template.html") as f:
    pdfoptions["footer_template"] = f.read()

mode = 4
if sys.argv[1:]:   # test if there are atleast 1 argument (beyond [0])
    mode = sys.argv[1]

def update_header(sec):
    subprocess.run(["sh","templates/settemplates.sh"])
    with open("exports/"+study_area+"/html/header_template.html",'r') as f:
        filedata = f.read()
        filedata = filedata.replace("[section]",section_names[sec])
    with open("exports/"+study_area+"/html/header_template.html",'w') as f:
        f.write(filedata)
    with open("exports/"+study_area+"/html/header_template.html") as f:
        pdfoptions["header_template"] = f.read()

def fix_css(fpath):
    "Removes the @page css tag from an html file"

    with open(fpath, "r") as fin, open(fpath+"temp", "w") as fout:
        lines = fin.readlines()
        wmode = 0
        for line in lines:
            if "@page {" in line:
                wmode = 3
            if wmode == 0:
                fout.write(line)
            elif wmode > 0:
                wmode -= 1
    os.remove(fpath)
    os.rename(fpath+"temp", fpath)


from playwright.sync_api import sync_playwright

def run(playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    page.emulate_media(media="screen")

    # Titlepage
    print("Converting titlepage.html to pdf..")
    page.goto("file://"+os.path.abspath(ipath+"titlepage.html"))
    page.pdf(path=opath+"titlepage.pdf", format=pdfoptions["format"])

    # OSM htmls
    if mode == 1 or mode == 3 or mode == 4:
        print("Converting 1a.html to pdf..")
        update_header("1a")
        fix_css(ipath+"1a.html")
        page.goto("file://"+os.path.abspath(ipath+"1a.html"))
        page.wait_for_timeout(1000)
        page.pdf(path=opath+"1a.pdf", **pdfoptions)

        print("Converting 1b.html to pdf..")
        update_header("1b")
        fix_css(ipath+"1b.html")
        page.goto("file://"+os.path.abspath(ipath+"1b.html"))
        page.wait_for_timeout(1000)
        page.pdf(path=opath+"1b.pdf", **pdfoptions)

    # REFERENCE htmls
    if mode == 2 or mode == 3 or mode == 4:
        print("Converting 2a.html to pdf..")
        update_header("2a")
        fix_css(ipath+"2a.html")
        page.goto("file://"+os.path.abspath(ipath+"2a.html"))
        page.wait_for_timeout(1000)
        page.pdf(path=opath+"2a.pdf", **pdfoptions)

        print("Converting 2b.html to pdf..")
        update_header("2b")
        fix_css(ipath+"2b.html")
        page.goto("file://"+os.path.abspath(ipath+"2b.html"))
        page.wait_for_timeout(1000)
        page.pdf(path=opath+"2b.pdf", **pdfoptions)

    # COMPARE htmls
    if mode == 3 or mode == 4:
        print("Converting 3a.html to pdf..")
        update_header("3a")
        fix_css(ipath+"3a.html")
        page.goto("file://"+os.path.abspath(ipath+"3a.html"))
        page.wait_for_timeout(1000)
        page.pdf(path=opath+"3a.pdf", **pdfoptions)
    if mode == 4:
        print("Converting 3b.html to pdf..")
        update_header("3b")
        fix_css(ipath+"3b.html")
        page.goto("file://"+os.path.abspath(ipath+"3b.html"))
        page.wait_for_timeout(1000)
        page.pdf(path=opath+"3b.pdf", **pdfoptions)

    browser.close()

with sync_playwright() as playwright:
    run(playwright)

# Stitch together
print("Stitching together single pdfs..")
args = ["gs", "-q", "-dNOPAUSE", "-dBATCH", "-dPDFSETTINGS=/prepress", "-sDEVICE=pdfwrite", "-sOutputFile=exports/"+study_area+"/pdf/report.pdf", "exports/"+study_area+"/pdf/titlepage.pdf"]
if mode >= 1: 
    args.append("exports/"+study_area+"/pdf/1a.pdf")
    args.append("exports/"+study_area+"/pdf/1b.pdf")
if mode >= 2:
    args.append("exports/"+study_area+"/pdf/2a.pdf")
    args.append("exports/"+study_area+"/pdf/2b.pdf")
if mode >= 3:
    args.append("exports/"+study_area+"/pdf/3a.pdf")
if mode >= 4:
    args.append("exports/"+study_area+"/pdf/3b.pdf")

subprocess.run(args)
args[4] = "-dPDFSETTINGS=/ebook"
args[6] = "-sOutputFile=exports/"+study_area+"/pdf/report_lowres.pdf"
subprocess.run(args)
print("Done! Created report.pdf and report_lowres.pdf in folder exports/[study_area]/pdf")
