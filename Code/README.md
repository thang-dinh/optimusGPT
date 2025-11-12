# Optimus GPT - Docker Setup

This project provides a two-service Docker setup with a main application and an isolated sandbox environment for executing AI-generated code.

## Prerequisites

- Docker and Docker Compose installed
- No local Poetry required; it runs inside the app container
- Ensure an `.env` file exists if your app expects it
- Prompts are enabled for interactive use

## Usage

### Build images

```bash
docker compose build
```

### Run main (foreground, prompts enabled)

```bash
docker compose up app
```

`main.py` will run in the container and may prompt for input() as usual.

When code is generated, the container logs will include a line like:
```
GENERATED_FILE::generated_code_iteration_1.py
```

The generated file is written to `./output_code` on the host.

### Run the generated code in an isolated sandbox (no network)

Replace `<filename>` below with the value printed in the previous step:

```bash
docker compose run --rm --network none executor python "/sandbox/code/<filename>"
```

This runs with:
- Read-only code mount
- No network access
- Dropped capabilities and no-new-privileges
- CPU and memory limits

## Notes

- This flow uses only Docker commands (no OS-specific shell scripts)
- The filename is manually copied from app logs into the executor command (by a developer or an external agent). This keeps the setup simple and cross-platform.
- `gurobipy` is included in the sandbox. If a valid Gurobi license is not available, imports may fail. Remove `gurobipy` from `executor.Dockerfile` if not needed.
- To add a writable temp area or timeouts later, we can extend the compose configuration with a tmp volume and use Python-level timeouts.