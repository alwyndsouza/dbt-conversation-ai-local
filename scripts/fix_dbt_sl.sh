#!/bin/bash

# Check and fix MetricFlow setup

echo "🔍 Checking MetricFlow Setup"
echo ""

# Check dbt version
echo "📦 Checking dbt version..."
if ! command -v dbt &> /dev/null; then
    echo "❌ dbt is not installed"
    echo "   Install: pip install dbt-core dbt-duckdb"
    exit 1
fi

dbt_version=$(dbt --version 2>&1 | grep "^dbt version" | head -1)
echo "   $dbt_version"

# Check if mf (MetricFlow CLI) command exists
echo ""
echo "🔧 Checking for 'mf' (MetricFlow CLI) command..."
if command -v mf &> /dev/null; then
    echo "✅ mf command is available"
    mf_version=$(mf --version 2>&1 | head -1)
    echo "   $mf_version"
else
    echo "❌ mf command is NOT available"
    echo ""
    echo "The 'mf' command is provided by the dbt-metricflow package."
    echo ""
    echo "Would you like to install dbt-metricflow? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo ""
        echo "📥 Installing dbt-metricflow..."
        pip install 'dbt-metricflow>=0.8.0'

        echo ""
        echo "✅ Installation complete!"
        echo ""
        echo "🔄 Verifying installation..."

        if command -v mf &> /dev/null; then
            echo "✅ mf command is now available!"
            mf_version=$(mf --version 2>&1 | head -1)
            echo "   $mf_version"
        else
            echo "⚠️  mf command still not available. You may need to:"
            echo "   1. Restart your terminal"
            echo "   2. Reactivate your virtual environment"
            echo "   3. Check for installation errors above"
        fi
    else
        echo ""
        echo "To install manually:"
        echo "   pip install 'dbt-metricflow>=0.8.0'"
        exit 1
    fi
fi

# Check if project is parsed
echo ""
echo "📄 Checking for manifest files..."
if [ -f "target/manifest.json" ]; then
    echo "✅ target/manifest.json exists"
else
    echo "⚠️  target/manifest.json not found"
    echo "   Run: dbt parse"
fi

if [ -f "target/semantic_manifest.json" ]; then
    echo "✅ target/semantic_manifest.json exists"
else
    echo "⚠️  target/semantic_manifest.json not found"
    echo "   Run: dbt parse"
fi

# Offer to run dbt parse
if [ ! -f "target/semantic_manifest.json" ]; then
    echo ""
    echo "Would you like to run 'dbt parse' now? (y/n)"
    read -r response

    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo ""
        echo "🔄 Running dbt parse..."
        dbt parse

        if [ -f "target/semantic_manifest.json" ]; then
            echo "✅ Semantic manifest created successfully!"
        else
            echo "⚠️  Parse completed but semantic_manifest.json not found"
            echo "   Check if you have semantic models defined in models/"
        fi
    fi
fi

# Test mf list metrics
echo ""
echo "🧪 Testing 'mf list metrics'..."
if mf list metrics &> /dev/null; then
    echo "✅ mf list metrics works!"
    echo ""
    echo "Available metrics:"
    mf list metrics | head -20
else
    echo "⚠️  'mf list metrics' failed"
    echo "   This is normal if you haven't defined any semantic models yet"
fi

echo ""
echo "="*50
echo "✅ Setup check complete!"
echo ""
echo "Next steps:"
echo "1. If mf is working, run: ./run_app.sh"
echo "2. If you just installed dbt-metricflow, restart your terminal first"
echo "3. Make sure you have semantic models in models/marts/"
echo "="*50
