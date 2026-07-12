# AI-Driven Cyber-Physical System

This course explores the integration of artificial intelligence with sensor technologies to create intelligent, adaptive cyber-physical systems capable of real-time perception, decision-making, and autonomous operation. As advances in edge computing and machine learning algorithms enable unprecedented levels of embedded intelligence, sensors evolve from passive data collectors to active components that process, fuse, and interpret information within networked environments. Students will examine AI techniques for sensor data processing, smart networking
protocols for distributed perception, perception-based robotic systems, and security challenges inherent in AI-
enabled physical systems, preparing them to design resilient systems for Industry 4.0, autonomous robotics, and
smart infrastructure applications.

# Requirements
- Python 3.9 or higher

# Create Conda Envirnment

We use conda environment for this project. You can install conda [Here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

To create the environment

```
conda create --file environment.yml
```

To Activate the environment

```
conda activate ee506
```

### Update Conda Env File

```
conda env export --no-builds --format=environment-yaml | grep -v "^prefix: " > environment.yml
```

# How to Run Sensorhub Simulator

[Check the ReadMe file here](sensorhub/README.md)

### Run the app

```
cd sensorhub && python -m uvicorn app:app --reload

```

### Presentations

- [1. Overview of AI-Driven CPS](https://html-preview.github.io/?url=https://github.com/kolithawarnakulasooriya/AI-driven-cyber-physical-system/blob/main/presentations/cps-ai-intro.html)
- [2. Sensors](https://html-preview.github.io/?url=https://github.com/kolithawarnakulasooriya/AI-driven-cyber-physical-system/blob/main/presentations/sensors-cps.html)
- [3. Kemlan Filtering](https://html-preview.github.io/?url=https://github.com/kolithawarnakulasooriya/AI-driven-cyber-physical-system/blob/main/presentations/kelman-filter-cps.html)
- [4. Machine Learning](https://htmlpreview.github.io/?https://github.com/kolithawarnakulasooriya/AI-driven-cyber-physical-system/blob/main/presentations/machine-learning-cps.html)
