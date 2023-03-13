## Prepares layer for SAM Build
## Download https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/stable-headless-chromium-amazonlinux-2.zip to chromium_layer
build-ChromiumLayer:
	mkdir "$(ARTIFACTS_DIR)/bin"
	mkdir "$(ARTIFACTS_DIR)/python"
	pip3 install -r layer_req.txt -t "$(ARTIFACTS_DIR)/python"
	cp chromedriver "$(ARTIFACTS_DIR)/bin"
	chmod +x "$(ARTIFACTS_DIR)/bin/chromedriver"
	curl -L https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/stable-headless-chromium-amazonlinux-2.zip -o chromium.zip
	unzip chromium.zip -d "$(ARTIFACTS_DIR)/bin"
