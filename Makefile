
BUILD_TIME := $(shell date +%Y-%m-%dT%T%z)
GIT_REV := $(shell git rev-parse --short HEAD)
PROJ_ROOT_DIR := $(dir $(realpath $(MKFILE_DIR)))

include ${PROJ_ROOT_DIR}version

# ======================================================
# Docker Inits
.PHONY: docker-init
docker-init:
	docker volume create production-demo-minio || true && \
	docker volume create production-demo-milvus-etcd || true && \
	docker volume create production-demo-milvus || true && \
	docker volume create production-demo-redis || true && \
	docker network create production-demo-network || true

# ======================================================
# Docker Builds

INGESTAPI_NAME := ingestapi
.PHONY: docker-build-ingestapi
docker-build-ingestapi:
	docker build . -f docker/Dockerfile.${INGESTAPI_NAME} -t production-demo/${INGESTAPI_NAME}:${VER} \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		--build-arg GIT_REV=$(GIT_REV) \
		--build-arg NAME=$(INGESTAPI_NAME) \
		--build-arg VER=$(VER)

INGESTWORKER_NAME := ingestworker
.PHONY: docker-build-ingestworker
docker-build-ingestworker:
	docker build . -f docker/Dockerfile.${INGESTWORKER_NAME} -t production-demo/${INGESTWORKER_NAME}:${VER} \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		--build-arg GIT_REV=$(GIT_REV) \
		--build-arg NAME=$(INGESTWORKER_NAME) \
		--build-arg VER=$(VER)

.PHONY: docker-build-ingestworker-cpu
docker-build-ingestworker-cpu:
	docker buildx build . -f docker/Dockerfile.${INGESTWORKER_NAME}.cpu \
		-t production-demo/${INGESTWORKER_NAME}:${VER}-cpu \
		--platform linux/amd64 \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		--build-arg GIT_REV=$(GIT_REV) \
		--build-arg NAME=$(INGESTWORKER_NAME) \
		--build-arg VER=$(VER)

SEARCHAPI_NAME := searchapi
.PHONY: docker-build-searchapi
docker-build-searchapi:
	docker build . -f docker/Dockerfile.${SEARCHAPI_NAME} -t production-demo/${SEARCHAPI_NAME}:${VER} \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		--build-arg GIT_REV=$(GIT_REV) \
		--build-arg NAME=$(SEARCHAPI_NAME) \
		--build-arg VER=$(VER)

.PHONY: docker-build-searchapi-cpu
docker-build-searchapi-cpu:
	docker buildx build . -f docker/Dockerfile.${SEARCHAPI_NAME}.cpu \
		-t production-demo/${SEARCHAPI_NAME}:${VER}-cpu \
		--platform linux/amd64 \
		--build-arg BUILD_TIME=$(BUILD_TIME) \
		--build-arg GIT_REV=$(GIT_REV) \
		--build-arg NAME=$(SEARCHAPI_NAME) \
		--build-arg VER=$(VER)
# ======================================================
# Docker Compose
.PHONY: docker-compose-up
docker-compose-up:
	export IMAGE_TAG=${VER} && \
	docker-compose up -d
		
.PHONY: docker-compose-down
docker-compose-down:
	export IMAGE_TAG=${VER} && \
	docker-compose down 

