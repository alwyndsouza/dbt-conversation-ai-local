#!/usr/bin/env python3
"""
Test Ollama setup for the Natural Language Semantic Layer Query App
"""

import sys

print("🔍 Testing Ollama Setup\n")

# Check if ollama package is installed
try:
    import ollama
    print("✅ ollama Python package installed")
except ImportError:
    print("❌ ollama Python package not installed")
    print("   Fix: pip install ollama")
    sys.exit(1)

# Check if Ollama is running
try:
    models = ollama.list()
    print("✅ Ollama is running")
except Exception as e:
    print(f"❌ Ollama is not running: {e}")
    print("   Fix: ollama serve")
    sys.exit(1)

# List available models
model_list = models.get('models', [])
if not model_list:
    print("❌ No models found")
    print("   Fix: ollama pull llama3.2")
    sys.exit(1)

# Get model names supporting both old and new API
model_names = [m['model'] if 'model' in m else m['name'] for m in model_list]

print(f"✅ Found {len(model_names)} model(s):")
for name in model_names:
    print(f"   • {name}")

# Test a simple query
print("\n🧪 Testing model with a simple query...")
recommended_models = [name for name in model_names if any(x in name for x in ['llama3.2', 'llama3.1', 'mistral'])]
test_model = recommended_models[0] if recommended_models else model_names[0]

print(f"   Using model: {test_model}")

try:
    response = ollama.generate(
        model=test_model,
        prompt='Return only valid JSON: {"metrics": ["total_revenue"], "group_by": ["month"]}',
        format='json',
        options={'temperature': 0.1}
    )
    print("✅ Model is responding correctly")
    resp_text = response['response'] if 'response' in response else getattr(response, 'response', '')
    print(f"   Response preview: {resp_text[:100]}...")
except Exception as e:
    print(f"❌ Model test failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✅ All checks passed! Ollama is ready to use.")
print("\nRecommended next steps:")
print("1. Run: ./scripts/run_app.sh")
print("2. Choose model: {test_model}")
print("4. Start asking questions!")
print("="*50)
