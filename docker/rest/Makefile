VERSION=v1
DOCKERUSER=dhairyaveera79

build:
	docker build -f Dockerfile -t demucs-rest .

push:
	docker tag demucs-rest $(DOCKERUSER)/demucs-rest:$(VERSION)
	docker push $(DOCKERUSER)/demucs-rest:$(VERSION)
	docker tag demucs-rest $(DOCKERUSER)/demucs-rest:latest
	docker push $(DOCKERUSER)/demucs-rest:latest
