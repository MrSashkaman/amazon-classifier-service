.PHONY: *


APP_PORT := 5004
DOCKER_IMAGE := amazon-clf
DOCKER_TAG:= latest

run_app:
	python -m uvicorn app:create_app --host='0.0.0.0' --port=$(APP_PORT)

install.prod:
	pip install -r requirements.txt

install.dev:
	pip install -r requirements.dev.txt

install: install.prod install.dev

download_weights:
	mkdir weights
	wget -O weights/amazon_classifier.onnx "https://www.dropbox.com/scl/fi/5j6bljutm4slln9e6y087/amazon_classifier.onnx?rlkey=6thykd0zvgsg16oiga6avmelg&st=44gii0ah&dl=0"

run_unit_tests:
	PYTHONPATH=. pytest tests/unit/

run_integration_tests:
	PYTHONPATH=. pytest tests/integration/

run_all_tests:
	make run_unit_tests
	make run_integration_tests

lint:
	flake8 src/
	flake8 tests/

build.prod:
	docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} --target prod .

build.dev:
	docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG}-dev --target dev .

build: build.prod build.dev

docker.run-tests:
	@echo ${YELLOW}"Run all tests in docker"${NC}
	@docker run -it --rm ${DOCKER_IMAGE}:${DOCKER_TAG}-dev make run_all_tests  || (echo ${RED}FAIL${NC} && exit 1)

docker.run-lint:
	@echo ${YELLOW}"Run linters in docker"${NC}
	@docker run -it --rm ${DOCKER_IMAGE}:${DOCKER_TAG}-dev make lint || (echo ${RED}FAIL${NC} && exit 1)

deploy:
	ansible-playbook -i inventory.ini deploy.yaml -k
destroy:
	ansible-playbook -i inventory.ini destroy.yaml -k

hw.docker-check: build docker.run-lint docker.run-tests
	@echo ${GREEN}"Dockerfile is correct"${NC}

docker.run-locally:
	docker run -d --name ${DOCKER_IMAGE}-app -p ${APP_PORT}:80 ${DOCKER_IMAGE}
