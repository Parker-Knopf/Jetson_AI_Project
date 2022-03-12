sudo apt install zip unzip
cd Jetson_AI_Project
unzip ssd-mobilenet.zip
mkdir model
cd model
mkdir objectPassword
cd ../
mv ssd-mobilenet.onnx ~/Jetson_AI_Project/model/objectPassword
mv labels.txt ~/Jetson_AI_Project/model/objectPassword
chmod +x start.sh