.PHONY: help generate-requirements deploy edit-version

help:  ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

generate-requirements:  ## generate requirements.txt from pyproject.toml with uv
	uv pip compile pyproject.toml -o requirements.txt

deploy:  ## Deploy the app locally
	uv run streamlit run Home_🏠.py

# Example: make version=0.0.1 edit-version
version?=0.0.1
edit-version:  ## Modify VERSION in src/utils.py and version pyproject.toml
	sed -i '' "s/^version = \".*\"/version = \"$(version)\"/" pyproject.toml
