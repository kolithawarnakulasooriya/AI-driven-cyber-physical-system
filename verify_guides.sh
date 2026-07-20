#!/bin/bash
# Simple verification script for the generated study guide directories and files
topics=("FalseDataInjecction" "Kelman filtering" "KNN" "LogisticRegression" "PolinomialRegresion" "Simple Regression")
missing=0
for topic in "${topics[@]}"; do
  if [ ! -f "presentation/$topic/study-guide.md" ]; then
    echo "❌ Missing: presentation/$topic/study-guide.md"
    missing=1
  else
    echo "✅ Present: presentation/$topic/study-guide.md"
  fi
done

if [ $missing -eq 0 ]; then
  echo "🎉 All study guides were generated successfully."
else
  echo "⚠️ Some study guides are missing."
fi