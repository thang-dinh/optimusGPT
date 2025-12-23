# Agent Flow Quick Reference

## Overview
OptimusGPT uses a multi-agent system to solve optimization problems with human-in-the-loop feedback.

## Files
- **AGENT_FLOW_DIAGRAM.md** - Comprehensive ASCII diagrams with detailed explanations
- **AGENT_FLOW_MERMAID.md** - Interactive Mermaid diagrams (renders on GitHub)
- **architectureFlow.txt** - High-level system architecture

## Agent Types

| Agent | Model | Purpose | Input | Output |
|-------|-------|---------|-------|--------|
| **Interpreter** | GPT-4o-mini | Parse problem | Problem statement | Structured problem (JSON) |
| **Solver** | GPT-4o-mini | Generate code | Formatted problem | Python code (gurobipy) |
| **Self-Check** | GPT-4o-mini | Validate solution | Problem + Solution | Quality summary |
| **Decision** | GPT-4o-mini | Choose strategy | Problem + Feedback + History | Next step (1/2/3) |
| **Execution** | PythonREPL | Run code | Python code | Execution output |

## Flow Paths

### Path 1: Initial Iteration (`path_initial`)
```
User Prompt → Interpreter → Solver → Execute → Self-Check → Output
```

### Path 2: Iterative with Feedback (`path_subsequent`)
```
Feedback → Decision Agent → [Strategy] → Self-Check → Output

Strategies:
  1. Reinterpret: Interpreter → Solver → Self-Check
  2. Solve Again: Solver → Self-Check
  3. Request Info: User Input → Recursive call
```

## Key Differences

| Aspect | Initial Flow | Iterative Flow |
|--------|-------------|----------------|
| **Code Execution** | ✅ Yes (PythonREPL) | ❌ No (Cases 1 & 2)* |
| **Self-Check Input** | Execution output | Code string |
| **User Interaction** | Simple yes/no | Context-aware decisions |

*Case 3 recursively calls back, eventually leading to execution

## Feedback Loops

### 1. Human-in-the-Loop
```
User → Feedback → Decision → Agents → Output → User
```

### 2. Information Gathering
```
Decision → "Need Info" → User → Decision (recursive)
```

### 3. Agent Chaining
```
Interpreter → Solver → Execution → Self-Check → Decision
```

## Decision Agent Strategy Selection

The Decision Agent chooses one of three strategies:

### Strategy 1: Reinterpret Problem
**When:** Problem understanding was incorrect
**Action:** Re-parse problem with feedback context, then solve
**Example:** User clarifies constraints or objectives

### Strategy 2: Solve Again
**When:** Problem understood correctly but solution approach failed
**Action:** Generate new code with current context
**Example:** User suggests different algorithm or parameters

### Strategy 3: Request Information
**When:** Missing critical information to proceed
**Action:** Ask user for specific details, then recurse
**Example:** Missing data, ambiguous requirements

## Code Locations

```
Code/
├── main.py                          # Entry point
├── agents/
│   ├── interpreter_agent.py         # Agent 1
│   ├── solver_agent.py              # Agent 2
│   ├── self_check_agent.py          # Agent 3
│   ├── iterative_decision_agent.py  # Agent 4
│   └── visualizer_agent.py          # (not in main flow)
└── agent_paths/
    └── iterative_solver.py          # Flow orchestration
```

## Usage Pattern

### First Iteration
```python
generated_code_output, self_check_summary = path_initial(user_prompt)
```

### Subsequent Iterations
```python
generated_code_output, self_check_summary = path_subsequent(
    user_prompt,
    previous_code_solution,
    previous_self_analysis,
    user_feedback
)
```

## Dependencies

- **LangChain** - Agent framework
- **OpenAI** - GPT-4o-mini model
- **gurobipy** - Optimization library
- **PythonREPL** - Code execution

## Visualization Options

1. **ASCII** (AGENT_FLOW_DIAGRAM.md)
   - ✅ Works everywhere
   - ✅ Version control friendly
   - ❌ Less visually appealing

2. **Mermaid** (AGENT_FLOW_MERMAID.md) ⭐ Recommended
   - ✅ Renders on GitHub automatically
   - ✅ Multiple diagram types (flowchart, sequence, state)
   - ✅ Interactive
   - ✅ Version control friendly
   - ✅ Export to PNG/SVG

3. **Other Tools** (see AGENT_FLOW_DIAGRAM.md)
   - PlantUML
   - Graphviz
   - Draw.io
   - Excalidraw
   - LucidChart/Figma

## Quick Commands

### View Mermaid Diagrams Online
```bash
# Copy Mermaid code from AGENT_FLOW_MERMAID.md
# Paste into: https://mermaid.live
```

### Check Code Flow
```bash
cd Code
python3 main.py  # Interactive execution
```

### Trace Agent Calls
Look for print statements in `iterative_solver.py`:
- Line 18: "Structured problem:"
- Line 35: "Solution:"
- Line 58: "Decision output:"
- Lines 63, 73, 83: Strategy selection

## Tips

1. **Start with Mermaid diagrams** for quick understanding
2. **Refer to ASCII diagrams** for detailed flow with edge cases
3. **Check architectureFlow.txt** for system architecture context
4. **Read agent files** to understand prompts and schemas
5. **Trace through iterative_solver.py** to see orchestration logic

## Common Patterns

### Pattern 1: Happy Path
```
User Request → Initial → Output → User Satisfied → Done
```

### Pattern 2: Single Refinement
```
User Request → Initial → Output → 
Feedback → Decision (Solve Again) → New Output → Done
```

### Pattern 3: Problem Reinterpretation
```
User Request → Initial → Output → 
Feedback → Decision (Reinterpret) → 
Interpreter → Solver → Output → Done
```

### Pattern 4: Iterative Refinement
```
User Request → Initial → Output → 
Feedback Loop (multiple iterations) → Done
```

### Pattern 5: Information Gathering
```
User Request → Initial → Output →
Feedback → Decision (Request Info) →
User Provides → Recursive Decision → ... → Done
```

## Extending the System

To add a new agent:
1. Create agent file in `agents/` (follow existing pattern)
2. Use structured output with Pydantic models
3. Update `iterative_solver.py` to call your agent
4. Update flow diagrams
5. Add to this quick reference

## Troubleshooting

- **Agent not responding:** Check environment variables in `.env`
- **Code execution timeout:** Increase timeout in `iterative_solver.py` line 34
- **Import errors:** Check `pyproject.toml` dependencies
- **Flow confusion:** Trace with print statements or check diagrams

## Resources

- GitHub: Mermaid renders automatically in `.md` files
- Mermaid Live Editor: https://mermaid.live
- LangChain Docs: https://python.langchain.com
- Gurobi Docs: https://www.gurobi.com/documentation/

---

For detailed diagrams, see:
- [ASCII Diagrams](./AGENT_FLOW_DIAGRAM.md)
- [Mermaid Diagrams](./AGENT_FLOW_MERMAID.md)
