import csv
import random
from collections import defaultdict
import pandas as pd
import plotly.graph_objects as go
import argparse

def read_csv(file_path, engine_col=0, weight_col=1, species_col=2):
    """
    Reads data from a CSV file and infers engine, weight, and species columns.
    """
    data = []
    engines = set()
    species = set()
    weight_totals = defaultdict(float)
    
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        
        for row in reader:
            if len(row) > species_col:
                engine = row[engine_col]
                species_item = row[species_col]
                weight = float(row[weight_col])
                
                engines.add(engine)
                species.add(species_item)
                
                data.append({
                    'source': engine,
                    'target': species_item,
                    'value': weight
                })
                
                weight_totals[(engine, species_item)] += weight
    
    return data, engines, species, weight_totals

def generate_colors(nodes):
    """
    Generates a random color for each node.
    """
    def random_color():
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    return {node: random_color() for node in nodes}

def format_data_for_sankeymatic(data, weight_totals, node_colors=None, flow_colors=None):
    """
    Formats the given data into the SankeyMATIC format.
    """
    formatted_data = "// Enter Flows between Nodes, like this:\n"
    
    for (source, target), total_weight in weight_totals.items():
        color = ''
        if flow_colors and (source, target) in flow_colors:
            color = f" {flow_colors[(source, target)]}"
        formatted_data += f"{source} [{total_weight:.2f}] {target}{color}\n"
    
    formatted_data += "\n// You can set a Node's color, like this:\n"
    
    if node_colors:
        for node, color in node_colors.items():
            formatted_data += f":{node} {color}\n"
    
    formatted_data += "\n// Use the controls below to customize\n// your diagram's appearance..."
    
    return formatted_data

def generate_r_code(file_path, source_col='Engine', target_col='Species', value_col='Weight'):
    """
    Generates R code for a Sankey diagram using networkD3 with flexible column names.
    """
    r_code = f"""
library(networkD3)
library(dplyr)
library(readr)

# Path to your CSV file
csv_file_path <- '{file_path}'

# Read the CSV file
data <- read_csv(csv_file_path)

# Aggregate weights by source and target
aggregated_data <- data %>%
  group_by({source_col}, {target_col}) %>%
  summarise(Weight = sum({value_col})) %>%
  ungroup()

# Create a unique list of nodes
nodes <- unique(c(aggregated_data${source_col}, aggregated_data${target_col}))
nodes_df <- data.frame(name = nodes)

# Map source and target to indices
aggregated_data <- aggregated_data %>%
  mutate(source = match({source_col}, nodes_df$name) - 1,
         target = match({target_col}, nodes_df$name) - 1)

# Create the Sankey diagram
sankey <- sankeyNetwork(
  Links = aggregated_data,
  Nodes = nodes_df,
  Source = "source",
  Target = "target",
  Value = "Weight",
  NodeID = "name",
  units = "Weight"
)

# Display the Sankey diagram
print(sankey)
"""
    return r_code

def generate_python_code(file_path, source_col='Engine', target_col='Species', value_col='Weight'):
    """
    Generates Python code for a Sankey diagram using plotly with flexible column names.
    """
    python_code = f"""
import pandas as pd
import plotly.graph_objects as go

# Read the CSV file
data = pd.read_csv('{file_path}')

# Aggregate weights by source and target
aggregated_data = data.groupby([source_col, target_col]).agg({{ value_col: 'sum' }}).reset_index()

# Create a unique list of nodes
nodes = list(pd.concat([aggregated_data[source_col], aggregated_data[target_col]]).unique())
node_indices = {{node: i for i, node in enumerate(nodes)}}

# Map source and target to indices
aggregated_data['source'] = aggregated_data[source_col].map(node_indices)
aggregated_data['target'] = aggregated_data[target_col].map(node_indices)

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=nodes
    ),
    link=dict(
        source=aggregated_data['source'],
        target=aggregated_data['target'],
        value=aggregated_data[value_col]
    )
)])

fig.update_layout(title_text="Sankey Diagram", font_size=10)
fig.show()
"""
    return python_code

def main():
    # Argument parsing
    parser = argparse.ArgumentParser(description='Generate Sankey diagram code.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file')
    parser.add_argument('--output', choices=['sankeymatic', 'python', 'r', 'all'], required=True, help='Output format')
    
    args = parser.parse_args()
    
    # Read data from CSV
    data, engines, species, weight_totals = read_csv(args.file_path)
    
    # Combine engines and species for node colors
    nodes = engines.union(species)
    
    # Generate colors for each node
    node_colors = generate_colors(nodes)
    
    # Optionally: Define specific colors for flows
    flow_colors = {}  # Example: {('Engine', 'Species'): '#FF0000'}
    
    # Generate and print the requested code
    if args.output in ['sankeymatic', 'all']:
        formatted_data = format_data_for_sankeymatic(data, weight_totals, node_colors, flow_colors)
        print("SankeyMATIC Format:")
        print(formatted_data)
    
    if args.output in ['python', 'all']:
        python_code = generate_python_code(args.file_path)
        print("\nPython Code for Sankey Diagram:")
        print(python_code)
    
    if args.output in ['r', 'all']:
        r_code = generate_r_code(args.file_path)
        print("\nR Code for Sankey Diagram:")
        print(r_code)

if __name__ == "__main__":
    main()

