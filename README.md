# Sankey Diagram Code Generator

This repository contains a Python script that reads (not-only) fisheries data from a CSV file and generates code snippets for creating Sankey diagrams in different formats. The script supports generating code for:

- **SankeyMATIC**: A [web-based tool](https://www.sankeymatic.com/) for creating Sankey diagrams.
- **Plotly (Python)**: An interactive plotting library for Python.
- **networkD3 (R)**: An R package for interactive network diagrams.

## Features

- **Flexible Input**: Handles CSV files with columns for source, target, and value.
- **Multiple Output Formats**: Generates code for SankeyMATIC, Plotly (Python), and networkD3 (R).
- **Customizable**: Allows specification of output format and node/flow colors.

## Using the Python Script
The Python script processes your CSV file and generates code snippets for various Sankey diagram formats. You can specify the desired output format using the `--output` option:

- **sankeymatic**: Generates code compatible with the SankeyMATIC web tool.
- **python**: Produces code for creating interactive Sankey diagrams in Python using Plotly.
- **r (networkD3)**: Creates code for generating Sankey diagrams in R using the networkD3 package.
- **all**: Outputs code snippets for all the above formats.

Example:   
```bash
  python sankey_formatter_all.py.py data.csv --output sankeymatic
```
