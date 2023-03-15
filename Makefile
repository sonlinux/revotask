build:
	@docker build --no-cache -t alisonmukoma/revtask:dev -f kubernetes/image/Dockerfile .
push:
	@docker push alisonmukoma/revtask:latest
render:
	@helm template -f kubernetes/chart/revotask/values.yaml kubernetes/chart/revotask > kubernetes/manifests/revotask.yaml
