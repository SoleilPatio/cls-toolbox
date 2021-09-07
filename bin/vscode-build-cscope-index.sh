#!/bin/bash

echo "Create cscope.files ..."
time cls_cscope_find.py -a    > .vscode/cscope/cscope.files
echo "Total files listed: "`wc -l .vscode/cscope/cscope.files` 
echo "Create ctags.files ..."
time cls_cscope_find.py       > ctags.files
echo "Total files listed: "`wc -l ctags.files` 


# -R : Recurse directories for files.
# -b : just build the database, and not launch the Cscope GUI
# -q : The -q causes an additional, 'inverted index' file to be created, which makes searches run much faster for large databases
# -k : -k sets Cscope's 'kernel' mode--it will not look in /usr/include for any header files that are #included in your source files 
#         (this is mainly useful when you are using Cscope with operating system and/or C library source code, as we are here).
# -L : Do a single search with line-oriented output.
# 
# cscope -d : standalone cscope GUI, not recreate database
# cscope: regenerate database w/o any flags
# cscope: cscope -q -k -L1 DRV_Reg32
# cscope UI:
#  exit:  Ctrl-d
echo "Building cscope ..."
pushd .vscode/cscope/
time cscope -Rbkq -i cscope.files
popd


# ctags (disable vscode plugin, not stable)
echo "Building ctags ..."
time ctags -R -f .tags -L ctags.files
rm tags
ln -s .tags tags
