# BlendFinder

## Overview
Python scripts for scanning a directory for all .blend files, generating a default camera or top-view preview of the active scene and exporting all objects using the .gltf format for easy viewing withing a Chrome browser based on a three.js renderer

## Usage
```
bf = BlendFinder("<your-path>") # init with your chosen directory
bf.list_blend_stats() # gather info on all blend files
bf.export_all_objects() # create output directory with all export and previews
```

## Viewing the results
After the export has been completed **output/BlendFinder_results.html** results will need to be opened with a chrome instance using specific flags, in order to avoid using a web server
```
chrome --disable-web-security  --user-data-dir="c:/tmp"
```

## Demo
The left sidebar will contain a list of previews for each .blend file that was found, while the exported .gltf object will be rendered using three.js
<img src="demo/animation.gif">