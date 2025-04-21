import yaml

# Load YAML file
with open('calibration_experiments.yaml', 'r', encoding='utf8') as file:
    data = yaml.safe_load(file)

# Now `data` contains a Python object (e.g., a dict or list)
print(yaml.dump(data, default_flow_style=False, sort_keys=False))
