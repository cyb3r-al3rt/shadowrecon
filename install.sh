#!/bin/bash
echo "🎭 ShadowRecon v1.0 - Installation"
echo "✅ No dependencies required - works with basic Python 3.8+"
echo "📦 Optional dependencies can enhance features"
pip3 install -r requirements.txt --user 2>/dev/null || echo "ℹ️ Running without optional dependencies"
chmod +x shadowrecon.py
echo "🚀 Ready to use: python3 shadowrecon.py -d example.com"
