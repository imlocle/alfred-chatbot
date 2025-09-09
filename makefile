# Usage:
# In order the switch between environments, you can specify the ENV variable.
# run make clean first!!!!

# $ make deploy ENV=dev
# $ make deploy ENV=prod
# $ make deploy            # defaults to dev
# $ make clean             # remove all build artifacts

.PHONY: deploy zip-all zip-layer zip-alfredask clean generate-backend-config

ENV ?= dev
BUILD_DIR = terraform/builds
LAYER_ZIP = $(BUILD_DIR)/python.zip
ALFRED_ASK = $(BUILD_DIR)/alfred_ask.zip
BACKEND_CONFIG_TMP = terraform/backend.auto.hcl

# Clean all build artifacts
clean:
	rm -f $(BUILD_DIR)/*.zip lambda_layer/python.zip terraform/backend.auto.hcl
	rm -rf lambda_layer/python

# Ensure build directory exists
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Zip Lambda layer using Docker (Amazon Linux 2)
zip-layer: $(BUILD_DIR)
	rm -rf lambda_layer/python
	mkdir -p lambda_layer/python
	docker run --rm \
		--platform linux/amd64 \
		-v $(CURDIR)/src:/var/task \
		-v $(CURDIR)/lambda_layer/python:/lambda/python \
		public.ecr.aws/sam/build-python3.13 \
		/bin/sh -c "pip3 install -r /var/task/requirements.txt -t /lambda/python --no-cache-dir"
	cd lambda_layer && zip -r ../$(LAYER_ZIP) python > /dev/null

# Zip full src directory for each Lambda
zip-alfredask: $(BUILD_DIR)
	cd src && zip -r ../$(ALFRED_ASK) . > /dev/null

# Run all zipping steps
zip-all: zip-layer zip-alfredask

# Generate dynamic backend config file
generate-backend-config:
	@echo "bucket = \"alfred-terraform-state-bucket\"" > $(BACKEND_CONFIG_TMP)
	@echo "key    = \"alfred/$(ENV)/terraform.tfstate\"" >> $(BACKEND_CONFIG_TMP)
	@echo "region = \"us-west-1\"" >> $(BACKEND_CONFIG_TMP)

# Deploy with Terraform
deploy: zip-all generate-backend-config
	@echo "🚀 Deploying to environment: $(ENV)"
	@rm -rf terraform/.terraform
	terraform -chdir=terraform init -backend-config=backend.auto.hcl
	terraform -chdir=terraform apply -var="environment=$(ENV)"