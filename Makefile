clean:		## delete pycache, build files
	@rm -rf deploy  
	@rm -rf layer 
	@rm -rf __pycache__

## prepares layer.zip archive for AWS Lambda Layer deploy 
chromium-layer-build: clean
	rm -f layer.zip
	mkdir layer layer/python
	cp -r bin layer/.
	curl -L https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F929513%2Fchrome-linux.zip?generation=1633657173061773\&alt=media -o chromium.zip
	cd layer/bin; unzip -u ../../chromium.zip
	pip3 install -r layer_req.txt -t layer/python
	cd layer; zip -9qr layer.zip .
	cp layer/layer.zip .
	rm -f chromium.zip
	rm -rf layer

## usage:	make BUCKET=your_bucket_name PROFILE=your-aws-profile upload-layers-to-stack-bucket
upload-layers-to-stack-bucket:
	aws s3 cp layer.zip s3://${BUCKET}/src/ChromiumLayer.zip --profile ${PROFILE}