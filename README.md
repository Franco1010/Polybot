## To update chromium layer
Run these commands in sequence:

`make chromium-layer-build` to prepare archive for AWS Lambda Layer deploy (layer.zip)

`make BUCKET=your_bucket_name PROFILE=your-aws-profile upload-layers-to-stack-bucket` to upload layer.zip to bucket