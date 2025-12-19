# Repository Guidelines

## Project Structure & Modules
- `flaco/` is the Python CLI and agent core (`cli.py`, `agent.py`, tools/, context/, llm/, database/); keep new logic beside its peers.
- `flaco-cli/` stores CLI notes/scripts and symlinks to the package code for convenience.
- `flaco-macos/` is the Electron app (main/preload/renderer) with tests under `flaco-macos/tests/*.test.js`.
- `docs/` holds guides plus private owner docs; avoid touching `docs/internal/` or `docs/archive/` unless intentional.
- `scripts/` provides install helpers; `.env.example` is the config template—keep real secrets out of git.

## Build, Test, and Development
- CLI setup: `python -m venv venv && source venv/bin/activate && pip install -e .`; run via `flaco` or `python -m flaco.cli --help`.
- Desktop: `cd flaco-macos && npm install && npm start`; `npm run build:quiet` mirrors CI, `npm run build:mac|win|linux` for installers.
- Mongo check: `pytest test_mongodb.py` (needs `MONGODB_URI`). Otherwise run `pytest` for unit suites.
- Keep dependencies lean; add shared helpers under `flaco/utils/` or existing desktop modules before pulling new packages.

## Coding Style & Naming Conventions
- Python: PEP 8 with 4-space indents, snake_case functions, CamelCase classes, type hints + docstrings for public APIs, and standard `logging` over prints.
- JavaScript: CommonJS in `flaco-macos`, camelCase variables, keep renderer-safe code in `preload.js`.
- Place new tests/docs near their feature; default to ASCII filenames/content.

## Testing Guidelines
- Use `pytest` with `test_*.py`; assert behavior, not logs. For coverage, run `pytest --cov=flaco --cov-report=html` on core changes.
- Desktop tests: `npm test` (runs settings/chat specs); add new `*.test.js` that stay headless and deterministic.
- Document external service needs (e.g., Mongo) in docstrings and gate with env checks when possible.

## Commit & Pull Request Guidelines
- Conventional commits (`feat:`, `fix:`, `docs:`) as noted in `CONTRIBUTING.md`.
- Branch from `main`, keep diffs scoped, update docs/config samples when behavior changes.
- PRs: short summary of behavior, tests run (CLI/desktop), linked issue, and screenshots/GIFs for UI changes.

## Security & Configuration Tips
- Create envs via `cp .env.example .env`; set `OLLAMA_URL`, `OLLAMA_MODEL`, `FLACO_PERMISSION_MODE`, `FLACO_MAX_ITERATIONS`, `FLACO_DEBUG`, and `MONGODB_URI` as needed.
- Never commit secrets or customer-only docs. Verify new features across permission modes (interactive/auto/headless) and prefer local-only defaults.
