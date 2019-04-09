# Exact matching off-line algorithm benchmarking

## About
The goal of this project is to compare the performance of the following algorithms:
- Suffix Array
- Suffix Tree
- Index sorted
- Index hash

Comparison was done by measuring the index structure build time, pattern querry time and memory usage.
The project contains implementations of these algorithms and a script that measures their performance.  

The following genomes were used to perform the tests:
- Mus pahari chromosome X
- Coffea arabica chromosome 1c
- Nothobranchius furzeri strain GRZ chromosome sgr01

## Project dependencies
Libraries that are used in this project are:
- matplotlib
- pandas
- numpy
- psutil

# Usage
To perform the benchmark tests, just run `main.py`.  
The results will be printed out in the console, written in Tests/Results/ directory and plotted in the diagrams.
