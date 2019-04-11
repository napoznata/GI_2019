# -------------------------------------------------- #
# Benchmarking

# Print operation progress in percent
progress_print = True

# Number of test iterations for each algorithm
num_of_test_iterations = 3

# Test file locations
performance_tests_dir_path = "Tests/Performance/"
performance_tests_results_dir = "Tests/Results/"

signature_file_dir = "machine_signature.txt"

# -------------------------------------------------- #
# Unit testing
unit_tests_dir_path = "Tests/Unit/"

# -------------------------------------------------- #
# Visualization

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
