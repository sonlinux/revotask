build:
	@docker build --no-cache -t alisonmukoma/revotask:dev -f kubernetes/image/Dockerfile .
push:
	@docker push alisonmukoma/revotask:latest
render:
	@helm template -f kubernetes/chart/revotask/values.yaml kubernetes/chart/revotask > kubernetes/manifests/revotask.yaml

deploy:
	@kubectl apply -f kubernetes/manifests/revotask.yaml
