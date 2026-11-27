# CS Academy

- Source of truth: `content/curriculum.yaml` and the unit YAML/asset files define the curriculum, questions, exercises and solutions. `docs/design.md` defines behavior and P0 scope. Follow `docs/sources.md` for attribution and use of external material.
- Done for P0 means a browser user can finish Lists, run Python with their own stdin and pass Docker tests, see a predict card in Review Arena on a later day, see XP and Daily quest progress, take Lists placement, and back up and restore progress.
- Run `make setup`, `make lint`, `make runner-image`, then `make test`. Use `make test-docker` to require Docker and the full TCP journey. Unit and integration tests isolate all writes in temporary directories.
- Verify the UI with `make run` at `http://127.0.0.1:4350`. The e2e server uses `127.0.0.1:4356`. Report browser, Docker, TCP and CI verification separately.
- Keep real learning data in the ignored, private `data/` directory. Store dated backups outside the repository. Never pass learner code to an interpreter on the host.
