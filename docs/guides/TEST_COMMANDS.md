# 🧪 Test Commands & Features

## Quick Actions (# commands)

Test these in flaco.cli:

```bash
# 1. Quick commit workflow
#Quick commit

# 2. Fresh start
#Fresh start

# 3. Code review
#Code review

# 4. Test and build
#Test and build

# 5. Status check
#Status check

# 6. Project scan
#Project scan
```

## Slash Commands

Test these in flaco.cli:

```bash
# Core commands
/help           # Should show all commands
/actions        # Should list quick actions
/status         # Should show current status
/setup          # Interactive setup wizard

# Configuration
/model          # Show current model
/models         # List available models
/permissions    # Show permission mode

# Project commands
/scan           # Scan project
/context        # Show FLACO.md
/init           # Create FLACO.md
/todos          # Show todos

# Git commands
/git status     # Git status
/git history    # Git history

# Agent commands
/agent list     # List agents
/agent current  # Show current agent

# Utils
/reset-config   # Reset configuration
/clear          # Clear screen
/reset          # Reset conversation
/exit           # Exit flaco
```

## Expected Behavior

### Quick Actions Should:
✅ Execute bash commands directly (not through agent)
✅ Show command output in real-time
✅ Display success/error messages
✅ Work with git commands

### Slash Commands Should:
✅ Execute instantly without agent processing
✅ Show proper output (tables, panels, etc.)
✅ Handle errors gracefully
✅ Navigate correctly (/help, /actions, etc.)

## Common Issues Fixed

1. **Quick actions calling agent** → Now executes bash directly
2. **Agent name mismatch** → Shows correct agent (e.g., Steve)
3. **Commands not found** → All 25 commands registered
4. **Git commands failing** → Direct subprocess execution

## Test Results

Run `flaco.cli` and test:

- [ ] `/help` shows all 25 commands
- [ ] `/actions` lists 6 quick actions
- [ ] `#Quick commit` executes git commands
- [ ] `/status` shows session info
- [ ] `/setup` runs wizard
- [ ] Agent name matches in header and metrics

If any fail, check:
1. Is venv activated?
2. Is package installed? (`pip install -e .`)
3. Any import errors? (`python -c "from flaco.cli import main"`)
