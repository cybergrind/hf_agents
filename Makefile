
check:
	pre-commit run --all-files

precommit:
	pre-commit run -s origin/main -o HEAD
