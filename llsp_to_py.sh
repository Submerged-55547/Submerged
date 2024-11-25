
dir=$(echo $1 | cut -d'/' -f1)
filename=$(echo $1 | cut -d'/' -f2)
pwd
echo "Converting $filename"
name=$(echo $filename | cut -d'.' -f1)
cd $dir
echo "I am in $pwd"
mkdir -p $name.tmp
cd $name.tmp
echo "I am now in $pwd"
ls -al ..
cp ../$filename .
tar -xvf $filename|| unzip $filename
cat projectbody.json|jq -r ".main" > $name.py
mv $name.py ..
echo "I am now here"
cd ..
rm -rf $name.tmp
cd ..
echo "I am now finally here"
exit 0
