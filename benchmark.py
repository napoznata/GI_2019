from algorithm import AlgorithmWithIndexStructure
import time
import threading
import psutil
import os
import copy
import gc
import sys
from config import *


class BenchmarkResult(object):

    def __init__(self, algorithm_name, text, pattern_set, init_time, patterns_query_time, used_memory):
        self.__algorithm_name = algorithm_name
        self.__text = text
        self.__pattern_set = pattern_set
        self.__init_time = init_time
        self.__patterns_query_time = patterns_query_time
        self.__used_memory = used_memory

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

    def get_memory_usage(self):
        return self.__used_memory

    def __repr__(self):
        return self.__str__()

    def __str__(self):



        return "--------------------------------------------------------------"\
               "\n" + self.__algorithm_name + " benchmark results \n\n" \
               "Used memory (bytes): \t" + str(self.__used_memory) + "\n" + \
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
        gc.collect()
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


class QueryThread(threading.Thread):

    def __init__(self, algorithm, pattern):
        threading.Thread.__init__(self)
        self.daemon = True
        self.__process = psutil.Process(os.getpid())
        self.__algorithm = algorithm
        self.__pattern = pattern

    def run(self):
        print("Query pattern \"" + self.__pattern + "\"...")

        self.__algorithm.query(self.__pattern)


class DummyAlgorithm(AlgorithmWithIndexStructure):

    def get_name(self):
        return "DummyAlgorithm"

    @staticmethod
    def __allocate_memory(size):
        x = bytearray(size//2)
        y = copy.deepcopy(x)
        del x
        return y

    def init_with_text(self, text):
        self.__allocate_memory(512000000)
        time.sleep(3)

    def query(self, pattern):
        self.__allocate_memory(256000000)
        time.sleep(1)


def benchmark_run(algorithm, text, patterns, title, iterations=1, memory_monitor_resolution=0.01):

    print("Running benchmark tests for " + title)

    min_init_time = sys.maxsize + 1
    min_total_query_time = sys.maxsize + 1
    min_memory_all = sys.maxsize + 1

    for i in range(iterations):

        print("\n---------- Test iteration " + str(i+1) + " ----------")
        alg_object = copy.deepcopy(algorithm)

        print("Building index structure...")

        mem_monitor = MemoryMonitor(memory_monitor_resolution)
        mem_monitor.start_monitoring()

        init_time_start = time.time()
        alg_object.init_with_text(text)
        init_time = time.time() - init_time_start

        min_init_time = min(min_init_time, init_time)

        query_threads = [QueryThread(alg_object, pattern) for pattern in patterns]
        time_start = time.time()
        for thr in query_threads:
            thr.start()
        for thr in query_threads:
            thr.join()
        total_query_time = time.time() - time_start

        min_total_query_time = min(min_total_query_time, total_query_time)
        min_memory_all = min(min_memory_all, mem_monitor.finish_monitoring())

        del alg_object

    return BenchmarkResult(title, text, patterns, min_init_time, min_total_query_time, min_memory_all)


class ProgressBar(object):

    __bar_value = 0
    __max_progress = 0
    __current_progress = 0
    __mutex = threading.Lock()

    def __init__(self, max_progress, title):
        self.__max_progress = max_progress
        if progress_print:
            ProgressBar.__mutex.acquire()
            print(title)
            ProgressBar.__mutex.release()


    def update_progress(self, progress):
        if self.__max_progress != 0:
            self.__current_progress = (progress / self.__max_progress) * 100
        else:
            raise Exception('Maximum progress must be greater than zero!')

        if progress_print:
            ProgressBar.__mutex.acquire()
            if self.__current_progress >= 100:
                print('')
            else:
                print('' * 100, end='\r')
                print('Progress: {:.2f}%'.format(self.__current_progress), end='')
            ProgressBar.__mutex.release()
