Import Settings
===============
.. _user-features-iosettings-import:

This section explains the import and export settings.

.. warning::
   Only a subset of these settings are currently used or fully supported even though they have been documented here. 
   This is due to the fact that they are ported directly from the old plugin and as such, will functionally remain the same.


Override Scene Information
--------------------------

.. _user-features-iosettings-import-override-info:

Overrides any existing niftools scene information with the data from the nif that is about to be imported.
See :ref:` Scene Settings<user-features-scene>` for information on what settings are available.

Keyframe File
-------------
.. _user-features-iosettings-import-keyframe:

Keyframe File ( .kf ) is an animation file using keyframe markers
A more complex animation file introduced with Skyrim ( .hkx ) is a havok based animation file, not supported by the plugin.


EGM File
--------
.. _user-features-iosettings-import-egm:

EGM files are a vertex morph animation file, most commonly used for facial animations and lip synch.

Animation
---------
.. _user-features-iosettings-import-animation:

Animation option, when selected, will import the :ref:`keyframe <user-features-iosettings-import-keyframe>` and/or the :ref:`EGM <user-features-iosettings-import-egm>` files listed in the file selection entries.


Align
-----
.. _user-features-iosettings-import-align:

Align selects how to align the tail position of non-parented bones to the root location.

Options are:

* Re-Align Tail Bone - Aligns the tail of non-parented bones to a uniform direction.
* Re-Align Tail Bone + roll - Sets a 90-degree roll to the tail after aligning. 

Process
-------
.. _user-features-iosettings-import-process:

Determines what parts of the file to import.

Import options include
* Everything - This will import geometry, armature, (keyframe, and EGM if set).
* Geometry only - Imports geometry and skips all other parts of the file.
* Skeleton only - Imports the armature and skips all other parts of the file.


Combine Shapes
--------------
.. _user-features-iosettings-import-combineshapes:

Select this option if you want all parts of a nif file to be imported as a single multi-part object. 
This is useful for keeping nifs organized when they contain several parts. As well as allowing for easier exporting of the nif.

Combine Vertices
----------------
.. _user-features-iosettings-import-combinevertex:

This options will combine vertices that contain the same x,y,z location and normal data into a single vertex.
* Select this when vertex ordering is not critical, non-animated objects or animated objects that use a skeleton for the animations, but do not contain morph animations.
* Do not use this for any object that uses morph type animations.

