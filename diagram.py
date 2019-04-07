import matplotlib.pyplot as pyplot
import pandas as pd
import numpy
from benchmark import BenchmarkResult

dummy_results = [BenchmarkResult('Suffix Array', '', '', 180, 3600, 2700, None),
                 BenchmarkResult('Suffix Tree', '', '', 200, 2500, 4000, None),
                 BenchmarkResult('Index Hash', '', '', 300, 5000, 3500, None),
                 BenchmarkResult('Index Sorted', '', '', 500, 6000, 1500, None)]

num_of_algorithms = 4

# Memory usage bar color for each algorithm
colors_memory_usage = [
    '#f4a261',
    '#F2D0A4',
    '#CC7E85',
    '#52965a']

# Init time bar color for each algorithm
colors_time_init = [
    (0.2, 0.7, 0.5),
    (0.2, 0.7, 0.5),
    (0.2, 0.7, 0.5),
    (0.2, 0.7, 0.5)]

# Additional brightness for query time bar
color_offset_query = 0.2

# The name kind of speaks for itself...
bar_thickness = 0.35

# Generate bar color for query time
colors_time_query = list([(r + color_offset_query, g + color_offset_query, b + color_offset_query)
                          for (r, g, b) in colors_time_init])


# Adds a diagram to the current plot window
# results - array of four BenchmarkResults, one for each algorithm
# title - title of the test
def plot_add_results(results, title):
    if len(results) != num_of_algorithms:
        print("Error: Plot must contain all four algorithms!")
        return

    names = [result.get_algorithm_name() for result in results]

    mem_usages = [result.get_memory_usage() for result in results]
    times_init = [result.get_init_time() for result in results]
    times_query = [result.get_patterns_query_time() for result in results]

    data = {"Memory usage (MB)": mem_usages, "Initialisation time (s)": times_init,
            "Query time (s)": times_query}
    df = pd.DataFrame(data, index=names)
    print(df)

    index = numpy.arange(num_of_algorithms)
    figure, axis = pyplot.subplots(2, 1, constrained_layout=True)

    # Plot memory usage
    axis[0].barh(index, mem_usages, bar_thickness, color=colors_memory_usage, align='center')
    axis[0].set_xlabel('Memory (MB)')
    axis[0].set_title("Memory usage")
    axis[0].set_yticks(index)
    axis[0].set_yticklabels(names)

    axis[1].barh(index, times_init, bar_thickness, color=colors_time_init, align='center', label='Initialization')
    axis[1].barh(index + bar_thickness, times_query, bar_thickness, color=colors_time_query, align='center',
                 label='Query time')
    axis[1].set_xlabel('Time (seconds)')
    axis[1].set_title("Execution time")
    axis[1].set_yticks(index)
    axis[1].set_yticklabels(names)
    axis[1].legend()

    figure.suptitle(title + '\n', fontsize=16)
    figure.canvas.set_window_title(title)


# Displays all the previously added plots in a separate window
def plot_show():
    pyplot.show()


# Usage:
#plot_add_results(dummy_results, 'Plot test')
#plot_add_results(dummy_results, 'Plot test')
#plot_show()
