# Run the script

You could use `uv` to run the script. Follow the next steps:
* Download the [data](https://github.com/stvno/stvno.github.io/raw/master/page/cliwoc/CLIWOC21.gpkg) to the same folder where the script is located.
* Modify the script if you want to add/remove/modify information in the final geojson file.
* Use [uv](https://docs.astral.sh/uv/getting-started/installation/) to run the script.
`uv run --with geopandas==1.1.0,antimeridian==0.4.1 --python 3.12 01_read_clean_simplify_gpkg.py`
