#!/bin/bash
echo "INFO:"
git diff --cached --name-only|grep llsp3| cut -d " " -f2 > .files
echo "DONE"
while IFS= read -r file_name || [ -n "$file_name" ];
do
echo "Procedding $file_name"
./llsp_to_py.sh $file_name
PY_FILENAME=$(echo $file_name|sed "s/.llsp3/.py/g")
echo "ADDING $PY_FILENAME"
git add $PY_FILENAME
done < <(cat .files)

exit 0
git diff --cached --name-only|grep llsp3| cut -d " " -f2|xargs ./llsp_to_py.sh
echo "Converted"
git diff --cached --name-only|grep llsp3| cut -d " " -f2|sed "s/.llsp3/.py/g"|xargs git add
echo "Added"
rm .files
