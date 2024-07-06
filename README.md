# blender-vmf-export by leaxcx
Script for Blender to export your geometry to .vmf (Valve Map Format)

## How to install:
  1. Download/clone repository
  2. Open Blender project, go to a "Scripting" tab
  3. "Text" -> "Open..."
  4. Open file "blender-vmf-export.py"
     
  At this point, you're pretty much done!

## How to make maps:
  1. Model your environment only with these shapes:
     1. Cube
     2. Icosphere
     3. Sphere
        
     These are the ones that are supported now!
  2. Map still should be properly sealed! You're still making a Source Engine map!
  3. Making sky is still recommended to do in Hammer Editor, because there's no such a thing (yet) as "Make Hollow" function.
  4. Map should be made out of non-contiguous convex shapes! Unfortunately, what you're doing in Blender is still limited by BSP (Binary Space Partition) limits.
  5. No n-gons!

(not nessesary, but life quality improver) In repository, there's a folder called "entities", at this point, there's only one there "info_player_start". It is a 1:1 scale reference model that allows you to easily scale your map to an actual Source Engine scale system.

     How to import "info_player_start":
     1. "File" -> "Append..."
     2. Choose "info_player_start reference.blend" -> "Object" -> "playerstart_reference"

## How to export:
  1. Set filepath
     
![filepath-here](https://github.com/leaxcx/blender-vmf-export/assets/172221284/8736c61c-fe24-4b5f-8df0-95fb80c97fa3)

  2. Press "Run Script" button
  
![play-button](https://github.com/leaxcx/blender-vmf-export/assets/172221284/c31934da-ea8d-4c7c-a1d7-e62843d61090)

  3. Done!

![exported-file](https://github.com/leaxcx/blender-vmf-export/assets/172221284/a542f7be-d7c0-4633-83cc-da067d3f6e7c)

## Known issues:
  1. Geometry flips vertically when exports to .vmf. 
    How to fix:

