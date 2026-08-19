.PHONY: smoke test

# Offline smoke: run a representative batch of solutions against known
# input/output cases and report pass/fail per problem.
smoke:
	python scripts/smoke.py

# Same cases as individual pytest tests.
test:
	python -m pytest tests/ -q
