#!/bin/bash
pip3 install -t ./function -r requirements.txt --system

cd function
zip -r ../function.zip .
cd ..

zip -r function.zip *.py

aws lambda update-function-code --function-name RegisterBot --zip-file fileb://function.zip