#!/bin/bash
set -e

# Topics
topics=("FalseDataInjecction" "Kelman filtering" "KNN" "LogisticRegression" "PolinomialRegresion" "Simple Regression")

# Create presentation directory
mkdir -p presentation

# Loop through topics
for topic in "${topics[@]}"; do
  echo "Creating directory for $topic"
  mkdir -p "presentation/$topic"
  echo "Copying study-guide-preparer.md to presentation/$topic/study-guide.md"
  cp .agents/agents/study-guide-preparer.md "presentation/$topic/study-guide.md"
done

echo "All study guides have been generated in the 'presentation' directory."