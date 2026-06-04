# Convenience wrapper around the pipeline. Mirrors run.sh stage-for-stage.
# Override the interpreter with: make PY=python
PY ?= py

.PHONY: all check acquire validate analyze figures clean

all: check

check:
	$(PY) src/check_env.py

# Stages are filled in as phases land (see CLAUDE.md §9).
acquire:
	$(PY) src/acquire/epoch_models.py
	$(PY) src/acquire/ca_cppa.py

validate:
	@echo "Phase 4: add src/validate/<source>.py invocations here."

analyze:
	@echo "Phase 5: add src/analyze/<question>.py invocations here."

figures:
	@echo "Phase 7: add src/viz/<figure>.py invocations here."

clean:
	@echo "Refusing to auto-delete. Remove results/ and figures/ by hand if intended;"
	@echo "data/raw/ is IMMUTABLE and must never be cleaned (CLAUDE.md §2.6)."
