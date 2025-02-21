
first:
	uv run first_agent

check:
	uv run pre-commit run --all-files

precommit:
	uv run pre-commit run -s origin/main -o HEAD
