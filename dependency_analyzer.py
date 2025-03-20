import json
import sys

def analyze_dependencies(json_file):
    with open(json_file, 'r') as f:
        deps = json.load(f)
    
    modules = {}
    
    # Calculate fan-in and fan-out
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
    
    # Find cyclic dependencies
    cycles = []
    for module, dependencies in deps.items():
        for dep in dependencies:
            if module in deps.get(dep, []):
                cycles.append((module, dep))
    
    # Sort by fan-in and fan-out
    sorted_by_fan_in = sorted(modules.items(), key=lambda x: x[1]['fan_in'], reverse=True)
    sorted_by_fan_out = sorted(modules.items(), key=lambda x: x[1]['fan_out'], reverse=True)
    
    # Print results
    print("=== Modules with highest fan-in (most depended upon) ===")
    for module, stats in sorted_by_fan_in[:10]:
        print(f"{module}: {stats['fan_in']} dependent modules")
    
    print("\n=== Modules with highest fan-out (most dependencies) ===")
    for module, stats in sorted_by_fan_out[:10]:
        print(f"{module}: {stats['fan_out']} dependencies")
    
    print("\n=== Potential cyclic dependencies ===")
    for m1, m2 in cycles:
        print(f"{m1} <--> {m2}")
    
    # Identify disconnected modules (no fan-in or fan-out)
    disconnected = [module for module, stats in modules.items() 
                   if stats['fan_in'] == 0 and stats['fan_out'] == 0]
    print("\n=== Disconnected modules ===")
    for module in disconnected:
        print(module)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dependency_analyzer.py <dependency_json_file>")
        sys.exit(1)
    analyze_dependencies(sys.argv[1])