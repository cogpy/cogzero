# OpenCog Integration for Agent Zero

This repository integrates OpenCog AGI framework with Agent Zero, providing advanced cognitive capabilities including knowledge representation, logical reasoning, and semantic memory.

## Overview

CogZero (Agent Zero with OpenCog) combines the flexibility of Agent Zero's agentic framework with OpenCog's powerful knowledge representation and reasoning capabilities.

## Features

### 1. Shared AtomSpace Manager
- **Singleton Pattern**: Ensures all OpenCog tools share the same AtomSpace within an agent context
- **Context Isolation**: Each agent conversation has its own isolated AtomSpace
- **Thread-Safe**: Uses locking to ensure safe concurrent access
- **Location**: `python/helpers/opencog_manager.py`

### 2. OpenCog Tools

#### OpenCogAtomSpace Tool
- Create and manage concepts, predicates, and links
- Query the knowledge base
- List and count atoms by type
- **Location**: `python/tools/opencog_atomspace.py`

#### OpenCogReasoning Tool  
- Forward and backward chaining inference
- Pattern matching
- Logical reasoning with inheritance and implication rules
- **Location**: `python/tools/opencog_reasoning.py`

#### OpenCogKnowledge Tool
- Import knowledge from text, JSON, and triple formats
- Export AtomSpace contents
- Load domain-specific knowledge (AI, science, common sense)
- **Location**: `python/tools/opencog_knowledge.py`

### 3. Automatic Initialization
- Agent initialization extension automatically sets up OpenCog
- Creates basic agent knowledge (type, capabilities)
- Loads configurable domain knowledge
- **Location**: `python/extensions/agent_init/_05_opencog_init.py`

## Installation

OpenCog packages are included in requirements.txt:

```bash
pip install -r requirements.txt
```

This will install:
- `opencog==5.0.3`
- `opencog-cogserver==5.0.3`

**Note**: OpenCog installation may require compilation and system dependencies. See [OpenCog Installation Guide](https://github.com/opencog/opencog) for platform-specific instructions.

## Configuration

OpenCog integration can be configured via the Settings UI or settings file:

### Settings

- **opencog_enabled** (bool, default: true): Enable/disable OpenCog integration
- **opencog_atomspace_persistence** (bool, default: false): Enable AtomSpace persistence
- **opencog_reasoning_engine** (string, default: "forward_chain"): Default reasoning method
- **opencog_default_domain** (string, default: ""): Domain knowledge to load on startup
  - Options: "AI", "science", "common_sense"
- **opencog_max_atoms** (int, default: 10000): Maximum atoms in AtomSpace
- **opencog_reasoning_steps** (int, default: 10): Max reasoning steps for inference

## Usage Examples

### Example 1: Building a Knowledge Base

```
User: Add some knowledge about animals to OpenCog

Agent uses opencog_atomspace tool:
- action: add_concept, name: "Dog"
- action: add_concept, name: "Cat"  
- action: add_concept, name: "Animal"

Agent uses opencog_reasoning tool:
- action: add_inheritance, child: "Dog", parent: "Animal"
- action: add_inheritance, child: "Cat", parent: "Animal"
```

### Example 2: Reasoning

```
User: If all animals need food, and a dog is an animal, does a dog need food?

Agent uses opencog_reasoning tool:
- action: add_implication, antecedent: "Animal", consequent: "NeedsFood"
- action: forward_chain, premises: ["Dog"]

Result: Yes, through inference Dog -> Animal -> NeedsFood
```

### Example 3: Domain Knowledge

```
User: Load AI domain knowledge

Agent uses opencog_knowledge tool:
- action: load_domain, domain: "AI"

This loads concepts like MachineLearning, NeuralNetwork, Agent, etc.
```

## Architecture

### Shared AtomSpace Pattern

The key innovation in this implementation is the shared AtomSpace manager:

```
┌─────────────────────────────────────┐
│   OpenCog Manager (Singleton)       │
│                                     │
│  ┌───────────┐  ┌───────────┐     │
│  │ Agent 1   │  │ Agent 2   │     │
│  │ AtomSpace │  │ AtomSpace │     │
│  └─────┬─────┘  └─────┬─────┘     │
│        │              │            │
└────────┼──────────────┼────────────┘
         │              │
    ┌────▼────┐    ┌────▼────┐
    │  Tool   │    │  Tool   │
    │ Instance│    │ Instance│
    └─────────┘    └─────────┘
```

### Without Shared Manager (Problem)
Each tool instance created its own AtomSpace, leading to:
- Knowledge added by opencog_atomspace not visible to opencog_reasoning
- No knowledge persistence across tool calls
- Waste of memory with duplicate AtomSpaces

### With Shared Manager (Solution)
All tools for the same agent share one AtomSpace:
- Knowledge persists across all tool invocations
- Tools can build upon each other's work
- Efficient memory usage
- Proper context isolation between different conversations

## Testing

Run OpenCog integration tests:

```bash
# All tests (skips OpenCog tests if not installed)
pytest tests/test_opencog_integration.py -v

# Only OpenCog tests (fails if OpenCog not installed)
pytest tests/test_opencog_integration.py -v -m opencog

# Summary test (shows what's installed)
pytest tests/test_opencog_integration.py::test_opencog_integration_summary -v -s
```

## Graceful Degradation

If OpenCog is not installed:
- Tools detect the missing package and return informative error messages
- Agent continues to function normally with other tools
- No crashes or exceptions
- Users are prompted to install OpenCog if they try to use those tools

## Limitations

Current implementation provides:
- ✅ Shared AtomSpace across tools
- ✅ Basic knowledge representation
- ✅ Simple forward/backward chaining
- ✅ Domain knowledge loading
- ⚠️ Pattern matching (basic string-based)
- ❌ PLN (Probabilistic Logic Networks) - requires opencog-pln
- ❌ Advanced reasoning engines
- ❌ Truth values and probabilities
- ❌ Attention allocation

## Future Enhancements

1. **Full PLN Integration**: Add probabilistic reasoning
2. **Persistence**: Save/load AtomSpace to disk
3. **Knowledge Import**: Better parsing of external knowledge sources
4. **Reasoning Optimization**: Implement more efficient pattern matching
5. **Multi-Agent Knowledge Sharing**: Allow agents to share knowledge
6. **Attention Allocation**: Implement OpenCog attention mechanics
7. **URE Integration**: Use the Unified Rule Engine for inference

## Contributing

To extend OpenCog integration:

1. **Add New Tools**: Create new tool files in `python/tools/`
2. **Add Tool Prompts**: Document in `prompts/agent.system.tool.<name>.md`
3. **Use Shared Manager**: Always use `get_opencog_manager()` to get AtomSpace
4. **Test**: Add tests in `tests/test_opencog_integration.py`

## References

- [OpenCog Project](https://opencog.org/)
- [OpenCog GitHub](https://github.com/opencog/opencog)
- [AtomSpace Documentation](https://wiki.opencog.org/w/AtomSpace)
- [Agent Zero Documentation](../docs/README.md)

## License

Same as Agent Zero - MIT License
