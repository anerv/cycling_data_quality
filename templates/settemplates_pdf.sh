#!/bin/bash

# Prepare header and footer templates for pdf report

area_name=$(grep "area_name:" config.yml | cut -d'"' -f 2)
area_name=${area_name##area_name: }
study_area=$(grep "study_area:" config.yml | cut -d'"' -f 2)
study_area=${study_area##study_area: }

cp templates/footer_metatemplate.html exports/"$study_area"/html/footer_template.html
cp templates/header_metatemplate.html exports/"$study_area"/html/header_template.html
footerheader_template=$(cat templates/footerheader_template.css | tr -s '\n' ' ')
sed -i "" -e "s/\[area_name\]/${area_name}/g" exports/"$study_area"/html/header_template.html
sed -i "" -e "s/\[footerheader_template\]/${footerheader_template}/g" exports/"$study_area"/html/footer_template.html