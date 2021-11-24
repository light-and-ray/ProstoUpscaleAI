#!/bin/sh

for file in ui/*.ui
do
    pyuic5 "$file" -o "src/Ui_`basename "$file" .ui`.py"
done
