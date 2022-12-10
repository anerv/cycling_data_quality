# Export all notebooks as HTML without code cells included

# One optional parameter possible, to choose mode:
# 1: Only generate 1a and 1b
# 2: Only generate 2a and 2b
# 3: Generate 1a+1b and 2a+2b and 3a
# 4: Generate 1a+1b and 2a+2b and 3a+3b (default)
# Example: sh export_notebooks2html.sh 3

if [[ -z $1 ]];
then 
    mode=4 # if run without parameter, choose mode 4
else
    mode=$1
fi

study_area_humanreadable=$(grep "study_area_humanreadable:" config.yml | cut -d'"' -f 2)
study_area_humanreadable=${study_area_humanreadable##study_area_humanreadable: }
study_area=$(grep "study_area:" config.yml | cut -d'"' -f 2)
study_area=${study_area##study_area: }

# Titlepage
cp templates/titlepage_template.html exports/"$study_area"/html/titlepage.html
sed -i "" -e "s/\[study_area_humanreadable\]/${study_area_humanreadable}/g" exports/"$study_area"/html/titlepage.html
sed -i "" -e "s/\[timestamp\]/$(date "+%Y-%m-%d %H:%M:%S")/g" exports/"$study_area"/html/titlepage.html
if [ $mode == 1 ];
then
	cp results/OSM/"$study_area"/maps_static/titleimage.png exports/"$study_area"/html/titleimage.png
elif [ $mode == 2 ];
then
	cp results/REFERENCE/"$study_area"/maps_static/titleimage.png exports/"$study_area"/html/titleimage.png
else
	cp results/COMPARE/"$study_area"/maps_static/titleimage.png exports/"$study_area"/html/titleimage.png
fi

# Single notebooks
if [ $mode == 1 ] || [ $mode == 3 ] || [ $mode == 4 ]; 
then
	# OSM notebooks
	jupyter nbconvert scripts/osm/1a_load_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
	mv scripts/osm/1a_load_osm.html exports/"$study_area"/html/1a.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/1a.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/1a.html

	jupyter nbconvert scripts/osm/1b_intrinsic_analysis_osm.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
	mv scripts/osm/1b_intrinsic_analysis_osm.html exports/"$study_area"/html/1b.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/1b.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/1b.html
fi

if [ $mode == 2 ] || [ $mode == 3 ] || [ $mode == 4 ]; 
then
	# REFERENCE notebooks
	jupyter nbconvert scripts/reference/2a_load_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
	mv scripts/reference/2a_load_reference.html exports/"$study_area"/html/2a.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/2a.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/2a.html

	jupyter nbconvert scripts/reference/2b_intrinsic_analysis_reference.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
	mv scripts/reference/2b_intrinsic_analysis_reference.html exports/"$study_area"/html/2b.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/2b.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/2b.html
fi

# COMPARE notebooks
if [ $mode == 3 ] || [ $mode == 4 ]; 
then
	jupyter nbconvert scripts/compare/3a_extrinsic_analysis_metrics.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
	mv scripts/compare/3a_extrinsic_analysis_metrics.html exports/"$study_area"/html/3a.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/3a.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/3a.html
fi

if [ $mode == 4 ]; 
then
	jupyter nbconvert scripts/compare/3b_extrinsic_analysis_feature_matching.ipynb --TagRemovePreprocessor.enabled=True --TagRemovePreprocessor.remove_cell_tags noex --no-input --to html
	mv scripts/compare/3b_extrinsic_analysis_feature_matching.html exports/"$study_area"/html/3b.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/3b.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/3b.html
fi
