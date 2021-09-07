@echo off

echo "Create cscope.files ..."
cls_cscope_find.py -aq > .vscode\cscope\cscope.files
echo "Total files listed:"
wc -l .vscode\cscope\cscope.files

@REM echo "Create ctags.files ..."
@REM cls_cscope_find.py > ctags.files
@REM echo "Total files listed:"
@REM wc -l ctags.files

echo "Building cscope ..."
cd .vscode\cscope\
cscope -Rbkq -i cscope.files
cd ..\..

@REM echo "Building ctags ..."
@REM ctags -R -f .tags -L ctags.files
