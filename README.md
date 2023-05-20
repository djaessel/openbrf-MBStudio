OpenBRF _by Marco Tarini_
------------------------

A modding tool used to view, edit and convert the proprietary _Binary Resource files_ (BRFs) loaded by the popular «Mount&Blade» and «Mount&Blade: Warband» games.

This GitHub repo was last updated from the source code ZIP file at:

https://forums.taleworlds.com/index.php?topic=72279.0

and modified to compile under Linux. Then it was fixed again by Swyter on early 2023 to also work on Windows and compile out-of-the-box, when opening it with compatible Qt Creator version like the one below:

https://download.qt.io/archive/qt/5.12/5.12.12/qt-opensource-windows-x86-5.12.12.exe.mirrorlist (**tip**: get offline before launching the installer to avoid creating a Qt account)

This version includes both a pre-generated version of `glew` 2.2.0 (the latest one at the time of writing) and `vcglib` 1.0.1 (the last compatible one) as a git submodule (*i.e.* a linked sub-repository pointing to a particular version instead of copying all those files over).

So make sure you initialize all submodules when you clone/download it. Plus, downloading it as a *.zip* file from GitHub will cause the `dependencies/vcglib` folder to be empty, so keep that in mind.

You don't need anything else, other than the open-source Qt5 SDK, that is the huge UI framework/SDK and build system OpenBRF is made of.

### License
This code and the original ZIP file are licensed under the _GNU
General Public License_, according to the dicussion forum:

https://forums.taleworlds.com/index.php?topic=72279.0

### Build instructions for Linux:

    # Now requires Qt5!
    qmake -makefile openBrf.pro
    make
    
    # run it overriding the float dot notation so that it can load
    # `carry_positions.txt` in other languages other than English
    env LC_NUMERIC=C ./openBrf

Alternatively there's also a ready-to-use _AUR_ package that might come in handy if you are using _Arch Linux_ (helpfully provided by Swyter):

https://aur.archlinux.org/packages/openbrf/
