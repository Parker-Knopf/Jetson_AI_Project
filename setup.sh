sudo apt install zip unzip
cd Object_Password_Prototype
unzip ssd-mobilenet.zip
mkdir model
cd model
mkdir shapes
cd ../
mv ssd-mobilenet.onnx ~/Object_Password_Prototype/model/shapes
mv labels.txt ~/Object_Password_Prototype/model/shapes
chmod +x run.sh