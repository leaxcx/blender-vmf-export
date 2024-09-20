# blender-vmf-export by leaxcx
## Blender addon to make maps for Source Engine

![ui-showcase](https://github.com/user-attachments/assets/0a4a5c43-6aa3-4710-9511-ae2669a822ff)

![example](https://github.com/leaxcx/blender-vmf-export/assets/172221284/cd51ab54-43ab-44c2-afdd-36ca676b6cbd)


## Create more complex shapes

![complex-shapes](https://github.com/leaxcx/blender-vmf-export/assets/172221284/6b565c32-1b5a-44e2-b225-2cbda0232b24)
  

## How to install:
  1. Download/clone repository
  2. Open Blender project, go to a "Scripting" tab
  3. "Text" -> "Open..."
  4. Open file "blender-vmf-export.py"
     
  At this point, you're pretty much done!

## How to make maps:
  Every mesh you want to export should be in collection named "brushes"!
  1. Model your environment only with these shapes:
     1. Cube
     2. Icosphere
     3. Sphere
        
     These are the ones that are supported now!
  2. Map still should be properly sealed! You're still making a Source Engine map!
  3. Making sky is still recommended to do in Hammer Editor, because there's no such a thing (yet) as "Make Hollow" function.
  4. Map should be made out of convex shapes! Unfortunately, what you're doing in Blender is still limited by BSP (Binary Space Partition) limits.
  5. Automatically, sky texture is set to "sky_day01_01" you can change it at line 27.

In repository, there's a folder called "entities", at this point, there's only one there "info_player_start". It is a 1:1 scale reference model that allows you to easily scale your map to an actual Source Engine scale system.

  How to import "info_player_start":
   1. "File" -> "Append..."
   2. Choose "info_player_start reference![ui-showcase](https://github.com/user-attachments/assets/65f660b5-b830-4c26-804f-8bece5d331e9)
.blend" -> "Object" -> "playerstart_reference"

Set "Clip End" to 10000 or more! It will improve visibility in Blender.

## How to export:
  1. Set filepath
     
![filepath-here](https://github.com/leaxcx/blender-vmf-export/assets/172221284/8736c61c-fe24-4b5f-8df0-95fb80c97fa3)

  2. Press "Run Script" button
  
![play-button](https://github.com/leaxcx/blender-vmf-export/assets/172221284/c31934da-ea8d-4c7c-a1d7-e62843d61090)

  3. Done!

![exported-file](https://github.com/leaxcx/blender-vmf-export/assets/172221284/a542f7be-d7c0-4633-83cc-da067d3f6e7c)

## Materials:
  Every mesh that does not have materials, in Hammer, will have "dev/dev_blendmeasure", but, if you mesh has material that has name like this "path/materialname" then it will automatically set material you've typed in Hammer.
  
  Example:

  ![material-example](https://github.com/leaxcx/blender-vmf-export/assets/172221284/749db8f1-423a-4cd5-b4fb-90f7cae7f265)

## UV scale:
  If you want your mesh to use its actual UV scale, and not default scale "0.25", create a new custom parameter (integer) in Object Properties called "useMeshUV" and set it to 1.

  ![useMeshUV-example](https://github.com/leaxcx/blender-vmf-export/assets/172221284/88084ec1-99fb-4ea9-b4d2-466caec2ff10)

## Known issues:
  1. Geometry flips vertically when exports to .vmf. 
    How to fix in Hammer:
    1. "Edit" -> "Select All"
    2. Press Ctrl+I or "Tools" -> "Flip Objects" -> "Vertically"
  2. No displacement support 
  3. No manual entity placement support in Blender (will be fixed soon)
  4. Fully rewrites file from scratch everytime you export it, so all entities/brushes you've placed in Hammer will be erased (also will be fixed soon)

There are some examples of test maps in folder called "files" (includes ".blend" and ".vmf" files"), so check it out if something gone wrong with it.

Good luck! :)


