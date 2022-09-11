
VERSION:=$(shell grep VERSION setup.py | head -n1 | cut -d"'" -f2)

.PHONY: build
build:
	echo $(VERSION)
	docker build -t cznewt/home-assistant-exporter .
	docker tag cznewt/home-assistant-exporter:latest cznewt/home-assistant-exporter:$(VERSION)

.PHONY: publish
publish:
	@docker push cznewt/home-assistant-exporter:$(VERSION)
	@docker push cznewt/home-assistant-exporter:latest
