from main import AlgorithmWithIndexStructure
import time
import threading
import psutil
import os


class BenchmarkResult(object):

    def __init__(self, algorithm_name, text, pattern_set, init_time, patterns_query_time, max_memory):
        self.__algorithm_name = algorithm_name
        self.__text = text
        self.__pattern_set = pattern_set
        self.__init_time = init_time
        self.__patterns_query_time = patterns_query_time
        self.__max_memory = max_memory

    def get_algorithm_name(self):
        return self.__algorithm_name

    def get_text(self):
        return self.__text

    def get_pattern_set(self):
        return self.__pattern_set

    def get_total_execution_time(self):
        return self.__init_time + self.__patterns_query_time

    def get_patterns_query_time(self):
        return self.__patterns_query_time

    def get_init_time(self):
        return self.__init_time

    def get_max_memory_usage(self):
        return self.__max_memory

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "--------------------------------------------------------------"\
               "\n" + self.__algorithm_name + " benchmark results \n\n" \
               "Max memory (bytes): \t" + str(self.__max_memory) + "\n" + \
               "Text init time: \t\t" + str(self.__init_time) + "\n" + \
               "Total query time: \t\t" + str(self.__patterns_query_time) + "\n" \
               "Total execution time: \t" + str(self.get_total_execution_time()) + "\n" \
               "--------------------------------------------------------------" \



class MemoryMonitor(threading.Thread):

    def __init__(self, refresh_rate):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__thread_running = threading.Event()
        self.__max_memory = 0
        self.__sleep_time = refresh_rate
        self.__process = psutil.Process(os.getpid())

    def run(self):
        initial_memory_usage = self.__process.memory_info().rss

        while self.__thread_running.isSet():
            current_memory_usage = self.__process.memory_info().rss - initial_memory_usage
            self.__max_memory = max(current_memory_usage, self.__max_memory)
            time.sleep(self.__sleep_time)

    def start_monitoring(self):
        self.__thread_running.set()
        self.start()

    def finish_monitoring(self):
        self.__thread_running.clear()
        return self.__max_memory

    def getName(self):
        return "MonitorThread #" + threading.Thread.getName(self)


class DummyAlgorithm(AlgorithmWithIndexStructure):

    def initWithText(self, text):
        bytearray(16000000)
        time.sleep(3)

    def query(self, pattern):
        bytearray(32000000)
        time.sleep(1)


def benchmark_run(algorithm, text, patterns, title, iterations=1, memory_monitor_resolution=0.01):

    print("Running benchmark tests for " + title)

    print("\nBuilding index structure...")
    total_query_time = 0
    mem_monitor_init = MemoryMonitor(memory_monitor_resolution)

    mem_monitor_init.start_monitoring()
    init_time_start = time.time()

    algorithm.initWithText(text)

    total_init_time = time.time() - init_time_start
    max_memory_all = mem_monitor_init.finish_monitoring()

    print("Execution time: \t\t" + str(total_init_time))
    print("Used memory: \t\t\t" + str(max_memory_all))

    for pattern in patterns:

        print("\nQuery pattern \"" + pattern + "\"", end='')
        max_time_pattern = 0
        memory_current_pattern = 0

        for i in range(iterations):

            print(".", end='')
            mem_monitor_pattern = MemoryMonitor(memory_monitor_resolution)

            mem_monitor_pattern.start_monitoring()
            time_start = time.time()

            algorithm.query(pattern)

            time_pattern = time.time() - time_start
            memory_current_pattern = mem_monitor_pattern.finish_monitoring()

            max_memory_all = max(max_memory_all, memory_current_pattern)
            max_time_pattern = max(max_time_pattern, time_pattern)

        total_query_time += max_time_pattern
        print("\nMax memory used: \t\t" + str(memory_current_pattern) + "\n" + "Max execution time: \t" + str(max_time_pattern))

    return BenchmarkResult(title, text, patterns, total_init_time, total_query_time, max_memory_all)


# Unit test for benchmark_run function

# Use a simulated exact match algorithm
dummy_algorithm = DummyAlgorithm()

# Simulate initial memory usage
bytearray(64000000)

results = benchmark_run(dummy_algorithm, "ACCTCGATCCGATCG", ["ATTG", "CCA"], "DummyAlgorithm", 1)

print("\n" + str(results))
