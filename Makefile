.PHONY: pipeline

server:
	mlflow server --host 0.0.0.0 --port 5000

pipeline:
	mlflow run .

pipeline_hpo:
	mlflow run . -P hydra_options="modeling.random_forest.max_depth=10,15 modeling.random_forest.n_estimators=200,500 modeling.max_tfidf_features=15,30 -m"

