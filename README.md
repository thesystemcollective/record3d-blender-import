# @thesystemcollective/record3d-blender-importer

This blend file contains a python script that imports the pose data from a record3d file into blender,
then generates an animation action on the currently selected object and applies the pose data on it.

### install:
```
git clone https://github.com/thesystemcollective/record3d-blender-importer
```

### usage:

copy your r3d file into this directory and rename it to data.r3d

open the blend file, import your object into it, select the object, then go to the scripts screen and press the play button of the record3d-blender-import.py script

alternatively, the record3d-blender-import.py script into your blender scene, select the object you want to animate,
then press the play button. Make sure that the data.r3d file exists in the directory of your blend file.

### debugging

as usual when using blender, open blender(.exe) from a terminal to get script debug information.