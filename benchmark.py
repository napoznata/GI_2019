from main import AlgorithmWithIndexStructure
import time
import threading
import psutil
import os


class BenchmarkResult(object):

    def __init__(self, algorithm_name, text, pattern, execution_time, max_memory):
        self.__algorithm_name = algorithm_name
        self.__text = text
        self.__pattern = pattern
        self.__time = execution_time
        self.__max_memory = max_memory

    def get_algorithm_name(self):
        return self.__algorithm_name

    def get_text(self):
        return self.__text

    def get_pattern(self):
        return self.__pattern

    def get_total_execution_time(self):
        return self.__time

    def get_max_memory_usage(self):
        return self.__max_memory


class MemoryMonitor(threading.Thread):

    def __init__(self, refresh_rate):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__thread_running = threading.Event()
        self.__max_memory = 0
        self.__sleep_time = refresh_rate
        self.__process = psutil.Process(os.getpid())

    def run(self):
        while self.__thread_running.isSet():
            current_memory_usage = self.__process.memory_info().rss
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


def benchmark_run(title, algorithm, text, pattern, iterations=1, memory_monitor_resolution=0.01):

    mem_monitor = MemoryMonitor(memory_monitor_resolution)

    max_memory_all = 0
    max_time = 0

    for i in range(iterations):

        mem_monitor.start_monitoring()
        time_start = time.time()

        algorithm.initWithText(text)
        algorithm.query(pattern)

        time_end = time.time()

        max_memory_current = mem_monitor.finish_monitoring()
        time_total = time_end - time_start

        max_memory_all = max(max_memory_all, max_memory_current)
        max_time = max(max_time,time_total)

    return BenchmarkResult(title, text, pattern, max_time, max_memory_all)

