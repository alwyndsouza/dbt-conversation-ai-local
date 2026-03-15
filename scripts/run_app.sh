#!/bin/bash

# Launch script for Natural Language Semantic Layer Query App

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Natural Language Semantic Layer Query App (Ollama Only)${NC}"
echo ""

# Check if Ollama is available
ollama_available=false

# Check Ollama
if command -v ollama &> /dev/null; then
    if ollama list &> /dev/null; then
        ollama_available=true
        echo -e "${GREEN}✅ Ollama is installed and running${NC}"
    else
        echo -e "${YELLOW}⚠️  Ollama is installed but not running${NC}"
        echo "   Start it with: ollama serve"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not installed${NC}"
    echo "   Install from: https://ollama.ai"
fi

echo ""

# If Ollama is not available, show setup instructions
if [ "$ollama_available" = false ]; then
    echo -e "${RED}❌ Ollama is not available!${NC}"
    echo ""
    echo -e "${BLUE}Setup Instructions:${NC}"
    echo ""
    echo "1. Install Ollama: https://ollama.ai"
    echo "2. Pull a model: ollama pull llama3.2"
    echo "3. Install Python package: pip install ollama"
    echo ""
    exit 1
fi

# Launch streamlit using uv
echo -e "${GREEN}✅ Launching app at http://localhost:8501${NC}"
echo ""
# Navigate to project root if script is run from scripts/
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Ensure dbt project is parsed
if [ ! -d "target" ] || [ ! -f "target/semantic_manifest.json" ]; then
    echo -e "${YELLOW}⚠️  dbt project not parsed yet or semantic manifest missing${NC}"
    echo ""
    echo "Running dbt parse..."
    uv run dbt parse
    echo ""
fi

uv run streamlit run streamlit_app.py
