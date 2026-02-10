#!/usr/bin/env python3
"""
Quick validation script for OpenCog integration in Agent Zero.

This script validates that:
1. OpenCog manager is available
2. All OpenCog tools can be imported
3. Settings include OpenCog configuration
4. Documentation files exist
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def check_manager():
    """Check if OpenCog manager is available."""
    print("✓ Checking OpenCog manager...")
    try:
        from python.helpers.opencog_manager import get_opencog_manager
        manager = get_opencog_manager()
        
        if manager.is_available():
            print("  ✅ OpenCog manager is available and OpenCog is installed")
            stats = manager.get_stats()
            print(f"     - AtomSpaces: {stats['atomspaces']}")
        else:
            print("  ⚠️  OpenCog manager is available but OpenCog is not installed")
            print("     Install with: pip install opencog==5.0.3 opencog-cogserver==5.0.3")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed to import OpenCog manager: {e}")
        return False


def check_tools():
    """Check if OpenCog tools can be imported."""
    print("\n✓ Checking OpenCog tools...")
    tools = [
        ("python.tools.opencog_atomspace", "OpenCogAtomSpace"),
        ("python.tools.opencog_reasoning", "OpenCogReasoning"),
        ("python.tools.opencog_knowledge", "OpenCogKnowledge"),
    ]
    
    all_ok = True
    for module_name, class_name in tools:
        try:
            module = __import__(module_name, fromlist=[class_name])
            tool_class = getattr(module, class_name)
            print(f"  ✅ {class_name} tool available")
        except Exception as e:
            print(f"  ❌ Failed to import {class_name}: {e}")
            all_ok = False
    
    return all_ok


def check_extension():
    """Check if OpenCog initialization extension exists."""
    print("\n✓ Checking OpenCog extension...")
    try:
        from python.extensions.agent_init import _05_opencog_init
        print("  ✅ OpenCog initialization extension available")
        return True
    except Exception as e:
        print(f"  ❌ Failed to import OpenCog extension: {e}")
        return False


def check_settings():
    """Check if settings include OpenCog configuration."""
    print("\n✓ Checking OpenCog settings...")
    try:
        from python.helpers.settings import get_default_settings
        settings = get_default_settings()
        
        required_settings = [
            "opencog_enabled",
            "opencog_atomspace_persistence",
            "opencog_reasoning_engine",
            "opencog_default_domain",
            "opencog_max_atoms",
            "opencog_reasoning_steps",
        ]
        
        missing = []
        for setting in required_settings:
            if setting not in settings:
                missing.append(setting)
        
        if missing:
            print(f"  ❌ Missing settings: {', '.join(missing)}")
            return False
        else:
            print(f"  ✅ All OpenCog settings present")
            print(f"     - opencog_enabled: {settings['opencog_enabled']}")
            print(f"     - opencog_reasoning_engine: {settings['opencog_reasoning_engine']}")
            return True
            
    except Exception as e:
        print(f"  ❌ Failed to check settings: {e}")
        return False


def check_documentation():
    """Check if documentation files exist."""
    print("\n✓ Checking documentation...")
    
    docs = [
        "docs/OPENCOG_INTEGRATION.md",
        "prompts/agent.system.tool.opencog_atomspace.md",
        "prompts/agent.system.tool.opencog_reasoning.md",
        "prompts/agent.system.tool.opencog_knowledge.md",
    ]
    
    all_ok = True
    for doc_path in docs:
        path = PROJECT_ROOT / doc_path
        if path.exists():
            print(f"  ✅ {doc_path}")
        else:
            print(f"  ❌ Missing: {doc_path}")
            all_ok = False
    
    return all_ok


def check_tests():
    """Check if tests exist."""
    print("\n✓ Checking tests...")
    
    test_file = PROJECT_ROOT / "tests" / "test_opencog_integration.py"
    if test_file.exists():
        print(f"  ✅ Integration tests exist")
        return True
    else:
        print(f"  ❌ Missing integration tests")
        return False


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("OpenCog Integration Validation")
    print("=" * 60)
    
    results = {
        "Manager": check_manager(),
        "Tools": check_tools(),
        "Extension": check_extension(),
        "Settings": check_settings(),
        "Documentation": check_documentation(),
        "Tests": check_tests(),
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for component, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{component:15} {status}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! OpenCog integration is properly configured.")
        return 0
    else:
        print("\n⚠️  Some checks failed. Review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
