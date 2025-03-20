import csv
import sys

def analyze_lcom(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        classes = []
        
        for row in reader:
            # Get basic info
            class_name = row.get('Type Name', '')
            package = row.get('Package Name', '')
            
            # Skip if empty
            if not class_name:
                continue
                
            # Parse LCOM values
            try:
                lcom1 = float(row.get('LCOM1', 0))
                lcom2 = float(row.get('LCOM2', 0))
                lcom3 = float(row.get('LCOM3', 0))
                lcom4 = float(row.get('LCOM4', 0))
                lcom5 = float(row.get('LCOM5', 0))
                yalcom = float(row.get('YALCOM', 0))
                
                # Add valid classes (with LCOM values)
                if lcom5 > 0 or (lcom1 > 0 and lcom3 > 1):
                    classes.append({
                        'name': class_name,
                        'package': package,
                        'full_name': f"{package}.{class_name}",
                        'lcom1': lcom1,
                        'lcom2': lcom2,
                        'lcom3': lcom3,
                        'lcom4': lcom4,
                        'lcom5': lcom5,
                        'yalcom': yalcom
                    })
            except (ValueError, TypeError):
                continue
        
        # Sort classes by LCOM5 for analysis
        high_cohesion_classes = sorted(classes, key=lambda x: x['lcom5'])[:5]
        low_cohesion_classes = sorted(classes, key=lambda x: x['lcom5'], reverse=True)[:5]
        
        # Print results in markdown table format
        print("## Classes with High Cohesion (Low LCOM values)")
        print("| Class Name | Package | LCOM1 | LCOM2 | LCOM3 | LCOM4 | LCOM5 | YALCOM |")
        print("|------------|---------|-------|-------|-------|-------|-------|--------|")
        for cls in high_cohesion_classes:
            print(f"| {cls['name']} | {cls['package']} | {cls['lcom1']:.1f} | {cls['lcom2']:.1f} | {cls['lcom3']:.1f} | {cls['lcom4']:.1f} | {cls['lcom5']:.3f} | {cls['yalcom']:.3f} |")
        
        print("\n## Classes with Low Cohesion (High LCOM values)")
        print("| Class Name | Package | LCOM1 | LCOM2 | LCOM3 | LCOM4 | LCOM5 | YALCOM |")
        print("|------------|---------|-------|-------|-------|-------|-------|--------|")
        for cls in low_cohesion_classes:
            print(f"| {cls['name']} | {cls['package']} | {cls['lcom1']:.1f} | {cls['lcom2']:.1f} | {cls['lcom3']:.1f} | {cls['lcom4']:.1f} | {cls['lcom5']:.3f} | {cls['yalcom']:.3f} |")
        
        # Find interesting examples for different LCOM metrics
        print("\n## Interesting Examples for Analysis")
        print("These classes show different patterns across LCOM metrics, good for discussion in lab report:")
        
        # Find classes with high LCOM1 but low LCOM5
        divergent = sorted([c for c in classes if c['lcom1'] > 100 and c['lcom5'] < 0.5], 
                          key=lambda x: x['lcom1'], reverse=True)[:3]
        
        if divergent:
            print("\n### Classes with high LCOM1 but low LCOM5")
            print("| Class Name | Package | LCOM1 | LCOM2 | LCOM3 | LCOM4 | LCOM5 | YALCOM |")
            print("|------------|---------|-------|-------|-------|-------|-------|--------|")
            for cls in divergent:
                print(f"| {cls['name']} | {cls['package']} | {cls['lcom1']:.1f} | {cls['lcom2']:.1f} | {cls['lcom3']:.1f} | {cls['lcom4']:.1f} | {cls['lcom5']:.3f} | {cls['yalcom']:.3f} |")
        
        # Find classes with very different LCOM5 and YALCOM
        diff_metrics = sorted([c for c in classes if abs(c['lcom5'] - c['yalcom']) > 0.5], 
                             key=lambda x: abs(x['lcom5'] - x['yalcom']), reverse=True)[:3]
        
        if diff_metrics:
            print("\n### Classes with very different LCOM5 and YALCOM values")
            print("| Class Name | Package | LCOM1 | LCOM2 | LCOM3 | LCOM4 | LCOM5 | YALCOM |")
            print("|------------|---------|-------|-------|-------|-------|-------|--------|")
            for cls in diff_metrics:
                print(f"| {cls['name']} | {cls['package']} | {cls['lcom1']:.1f} | {cls['lcom2']:.1f} | {cls['lcom3']:.1f} | {cls['lcom4']:.1f} | {cls['lcom5']:.3f} | {cls['yalcom']:.3f} |")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_guava_lcom.py <csv_file>")
        sys.exit(1)
    analyze_lcom(sys.argv[1])
