# blender-vmf-export by leaxcx
## Blender addon to make maps for Source Engine

![example](https://github.com/leaxcx/blender-vmf-export/assets/172221284/cd51ab54-43ab-44c2-afdd-36ca676b6cbd)

![ui-showcase](https://github.com/user-attachments/assets/0a4a5c43-6aa3-4710-9511-ae2669a822ff)


## Create more complex shapes

![complex-shapes](https://github.com/leaxcx/blender-vmf-export/assets/172221284/6b565c32-1b5a-44e2-b225-2cbda0232b24)
  

## How to install:
  1. Download/clone repository
  2. Open Blender project, Go to the Edit menu at the top of the screen.
  3. Select Preferences.
  4. In the Preferences window, select the Add-ons tab on the left sidebar.
  5. Click on the Install... button at the top of the window.
  6. Open file "blender-vmf-export.py"

  I also added "shortcut addons", which is not nessesary to install, just life quality improvement things:
  1. "fast-material-picker.py" - creates additional panel with all materials in your scene with button "Assign to Selected Face". When your project has a lot of materials, it helps.

     ![ui-materials](https://github.com/user-attachments/assets/098097e9-18d2-4d89-9bb4-6d475afe5801)

  
  3. "shortcut-convex.py" - creates additional panel with button "Make Mesh Convex" automatically makes mesh convex, which means ready for .vmf export.

     ![ui-convex](https://github.com/user-attachments/assets/20866d4a-ad9b-41a6-96bc-85bac909361a)


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
  4. Map should be made out of convex shapes! Unfortunately, what you're doing in Blender is still limited by BSP limits.
  5. Automatically, sky texture is set to "sky_day01_01" you should change it by hand in Hammer (soon).
  6. Checkmark "Rename Objects to IDs" automatically names brushes as "brush_1", "brush_2", "brush_3", etc... Not nessesary, but i find it generally easier to manipulate geometry when it's sorted.

In repository, there's a folder called "entities", at this point, there's only one there "info_player_start". It is a 1:1 scale reference model that allows you to easily scale your map to an actual Source Engine scale system.

  How to import "info_player_start":
   1. "File" -> "Append..."
   2. Choose "info_player_start reference
.blend" -> "Object" -> "playerstart_reference"

Set "Clip End" to 10000 or more! It will improve visibility in Blender.

## How to export:
  1. Set filepath (with yourfilename.vmf in the end)
     
![ui-export](https://github.com/user-attachments/assets/a44f90e5-3924-4133-8c2f-16e6760bf2df)

  2. Press "Export VMF" button

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


