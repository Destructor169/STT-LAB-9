# Module Dependency and Cohesion Analysis  
**Course:** CS202 Software Tools and Techniques for CSE  
**Date:** 20th March 2025  

---

## Table of Contents
1. [Introduction](#introduction)  
2. [Tools Used](#tools-used)  
3. [Python Dependency Analysis](#python-dependency-analysis)  
4. [Java LCOM Analysis](#java-lcom-analysis)  
5. [Conclusions and Recommendations](#conclusions-and-recommendations)  
6. [Code Used](#code-used)  

---

## Introduction
This lab focuses on analyzing software dependencies and cohesion using **pydeps** (for Python) and **LCOM** (Lack of Cohesion of Methods) for Java. The primary objectives were:  
- Using **pydeps** to generate and analyze dependency graphs for Python projects  
- Using **LCOM** to measure class cohesion in Java projects  
- Identifying design flaws and code smells (anti-patterns)  
- Implementing modularization and refactoring strategies to optimize software structure  

---

## Tools Used
### For Python Analysis:
- **Python 3.x**  
- **pydeps**  
- **Custom dependency analyzer script**  

### For Java Analysis:
- **Java JDK 17**  
- **LCOM analysis tool**  
- **Custom LCOM analysis script**  

### Projects Analyzed:
- **Flask** web framework (Python)  
- **Google Guava** library (Java)  

---

## Python Dependency Analysis
### Methodology
1. Used **pydeps** to generate a dependency graph.  
2. Generated JSON data using the `--show-deps` option.  
3. Created a custom analyzer script to calculate **fan-in** and **fan-out** metrics.  
4. Identified **cyclic dependencies** and **disconnected modules**.  

### Key Findings
- **Modules with Highest Fan-in** (most depended upon):  
    - `bacon`: 22 dependent modules  
    - `name`: 22 dependent modules  
    - `path`: 22 dependent modules  

- **Modules with Highest Fan-out** (most dependencies):  
    - `flask`: 5 dependencies  
    - `flask.__main__`: 5 dependencies  
    - `flask.app`: 5 dependencies  
    - `flask.blueprints`: 5 dependencies  

- **Cyclic Dependencies:**  
    - ✅ No cyclic dependencies found  

- **Disconnected Modules:**  
    - ✅ No disconnected modules found  

### Dependency Impact Assessment
Changes to high fan-in modules (`bacon`, `name`, `path`) would require careful testing to avoid breaking functionality in 22 dependent modules.  

---

## Java LCOM Analysis
### Methodology
1. The cohesion analysis was performed using the **LCOM tool**.  
2. LCOM metrics (LCOM1-5 and YALCOM) were calculated for each class.  

### Understanding LCOM Metrics
| Metric | Description |
|--------|-------------|
| **LCOM1** | Counts method pairs not sharing instance variables (higher = worse) |
| **LCOM2** | Refined version of LCOM1 |
| **LCOM3** | Counts connected components in method-attribute graph |
| **LCOM4** | Like LCOM3 but considers method-method calls |
| **LCOM5** | Normalized (0-1), higher values indicate less cohesion |
| **YALCOM** | "Yet Another LCOM" - alternative normalized measure |

### Key Findings
#### **Classes with High Cohesion (Low LCOM values):**  
| Class Name | Package | LCOM1 | LCOM2 | LCOM3 | LCOM4 | LCOM5 | YALCOM |
|-----------|---------|-------|-------|-------|-------|-------|--------|
| LittleEndianDataInputStream | com.google.common.io | 136.0 | 0.0 | 17.0 | 8.0 | 0.000 | 0.471 |
| Base64Encoding | com.google.common.io | 10.0 | 0.0 | 5.0 | 5.0 | 0.000 | 0.000 |
| ByteArrayDataOutput | com.google.common.io | 105.0 | 0.0 | 15.0 | 15.0 | 0.000 | -1.000 |

#### **Classes with Low Cohesion (High LCOM values):**  
| Class Name | Package | LCOM1 | LCOM2 | LCOM3 | LCOM4 | LCOM5 | YALCOM |
|-----------|---------|-------|-------|-------|-------|-------|--------|
| EmptyCharSource | com.google.common.io | 1.0 | 0.0 | 2.0 | 2.0 | 2.000 | 1.000 |
| HttpHeaders | com.google.common.net | 1.0 | 0.0 | 2.0 | 2.0 | 2.000 | 1.000 |
| ContainsPatternFromStringPredicate | com.google.common.base | 1.0 | 0.0 | 2.0 | 2.0 | 2.000 | 1.000 |

#### **Interesting Class Patterns:**  
| Class Name | Package | LCOM1 | LCOM2 | LCOM3 | LCOM4 | LCOM5 | YALCOM |
|-----------|---------|-------|-------|-------|-------|-------|--------|
| Preconditions | com.google.common.base | 3486.0 | 0.0 | 84.0 | 78.0 | 0.000 | 0.929 |
| AbstractNetwork | com.google.common.graph | 630.0 | 0.0 | 36.0 | 17.0 | 0.000 | 0.472 |
| Network | com.google.common.graph | 406.0 | 0.0 | 29.0 | 29.0 | 0.000 | -1.000 |

### Implications of High LCOM Values:
- **Multiple Responsibilities:**  
  - Class is likely doing too many unrelated things.  
- **Potential for Class Extraction:**  
  - Groups of unrelated methods suggest opportunities for refactoring.  
- **Poor Encapsulation:**  
  - High LCOM may indicate poor encapsulation and code smell.  

---

## Conclusions and Recommendations
### ✅ **Python Dependencies:**
- No cyclic dependencies (good for maintainability)  
- Consistent fan-out patterns (disciplined design)  
- Well-defined core modules (with high fan-in)  

### ✅ **Java Cohesion:**
- Several classes with excellent cohesion (LCOM5 = 0)  
- Some classes with poor cohesion that could benefit from refactoring  

### 🔧 **Refactoring Recommendations:**
- **Extract Method:** Move cohesive segments into separate methods  
- **Extract Class:** Split class into multiple cohesive classes  
- **Move Method:** Relocate methods to more appropriate classes  
- **Decrease Class Scope:** Narrow class responsibility  

---

## Code Used
### Python Dependency Analyzer
```python
import json
import sys

def analyze_dependencies(json_file):
    with open(json_file, 'r') as f:
        deps = json.load(f)
    
    modules = {}
    
    for module, dependencies in deps.items():
        if module not in modules:
            modules[module] = {'fan_in': 0, 'fan_out': len(dependencies)}
        else:
            modules[module]['fan_out'] = len(dependencies)
        
        for dep in dependencies:
            if dep not in modules:
                modules[dep] = {'fan_in': 1, 'fan_out': 0}
            else:
                modules[dep]['fan_in'] += 1

    sorted_by_fan_in = sorted(modules.items(), key=lambda x: x[1]['fan_in'], reverse=True)
    sorted_by_fan_out = sorted(modules.items(), key=lambda x: x[1]['fan_out'], reverse=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dependency_analyzer.py <dependency_json_file>")
        sys.exit(1)
    analyze_dependencies(sys.argv[1])
