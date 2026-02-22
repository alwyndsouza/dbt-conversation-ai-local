#!/usr/bin/env python3
"""
Pre-flight check for Natural Language Semantic Layer Query App
Run this before launching the Streamlit app to verify everything is set up correctly
"""

import sys
import subprocess
import os
from pathlib import Path

def check(name, condition, fix_msg=""):
    """Check a condition and print result"""
    if condition:
        print(f"✅ {name}")
        return True
    else:
        print(f"❌ {name}")
        if fix_msg:
            print(f"   Fix: {fix_msg}")
        return False

def run_command(cmd):
    """Run a command and return True if successful"""
    try:
        subprocess.run(cmd, capture_output=True, check=True, timeout=10)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return False

def main():
    print("🔍 Pre-flight check for Natural Language Semantic Layer Query App\n")

    all_checks_passed = True

    # Check Python version
    version = sys.version_info
    python_ok = (3, 9) <= (version.major, version.minor) <= (3, 12)
    all_checks_passed &= check(
        f"Python version (3.9-3.12): {version.major}.{version.minor}",
        python_ok,
        "Use Python 3.9-3.12. Current version may have compatibility issues."
    )

    # Check required packages
    packages = {
        'dbt-core': ['dbt', '--version'],
        'streamlit': ['streamlit', '--version'],
        'ollama (Python)': [sys.executable, '-c', 'import ollama'],
        'plotly': [sys.executable, '-c', 'import plotly'],
        'pandas': [sys.executable, '-c', 'import pandas'],
        'dbt-metricflow': ['mf', '--version'],
    }

    for pkg, cmd in packages.items():
        all_checks_passed &= check(
            f"Package/CLI installed: {pkg}",
            run_command(cmd),
            f"Run: pip install {pkg.split(' ')[0]}"
        )

    # Check Ollama service
    all_checks_passed &= check(
        "Ollama service running",
        run_command(['ollama', 'list']),
        "Start Ollama service (ollama serve)"
    )

    # Check dbt project files
    all_checks_passed &= check(
        "dbt_project.yml exists",
        Path('dbt_project.yml').exists(),
        "Make sure you're in the dbt project directory"
    )

    # Check if dbt has been parsed
    target_dir = Path('target')
    manifest = target_dir / 'manifest.json'
    all_checks_passed &= check(
        "dbt project parsed (target/manifest.json exists)",
        manifest.exists(),
        "Run: dbt parse"
    )

    # Check if semantic models exist
    semantic_models_path = Path('target/semantic_manifest.json')
    all_checks_passed &= check(
        "Semantic models parsed (target/semantic_manifest.json exists)",
        semantic_models_path.exists(),
        "Run: dbt parse"
    )

    # Check if streamlit app file exists
    all_checks_passed &= check(
        "streamlit_app.py exists",
        Path('streamlit_app.py').exists(),
        "Make sure streamlit_app.py is in the root directory"
    )

    print("\n" + "="*60)

    if all_checks_passed:
        print("✅ All checks passed! Ready to launch the app.")
        print("\nTo start the app, run:")
        print("  ./scripts/run_app.sh")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nQuick fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Start Ollama and pull a model: ollama pull llama3.2")
        print("  3. Parse dbt: dbt parse")
        return 1

if __name__ == '__main__':
    # Ensure we are in the project root
    if not Path('dbt_project.yml').exists() and Path('../dbt_project.yml').exists():
        os.chdir('..')
    sys.exit(main())
