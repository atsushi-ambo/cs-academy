.PHONY: setup run test test-unit test-web test-docker lint backup restore runner-image audit

setup:
	uv sync --locked

run:
	uv run --locked python -m app run

test: test-web
	uv run --locked python -m unittest -v

test-web:
	node --experimental-vm-modules --test tests/test_web.mjs

test-unit:
	uv run --locked python -m unittest -v tests.test_content tests.test_fsrs tests.test_learning tests.test_http tests.test_runner

test-docker:
	CS_ACADEMY_REQUIRE_DOCKER=1 uv run --locked python -m unittest -v tests.test_docker

lint:
	uvx --python 3.13 ruff@0.15.22 check app runner tests
	uv run --locked python -m app validate

backup:
	uv run --locked python -m app backup

restore:
	uv run --locked python -m app restore "$$BACKUP"

runner-image:
	docker build --tag cs-academy-runner:p0 runner

audit:
	@requirements=$$(mktemp); trap 'rm -f "$$requirements"' EXIT; \
		uv export --locked --no-dev --no-emit-project --no-header --format requirements.txt > "$$requirements" && \
		uvx --python 3.13 pip-audit@2.10.1 --require-hashes --disable-pip --no-deps -r "$$requirements"
