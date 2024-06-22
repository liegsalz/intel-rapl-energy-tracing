import multiprocessing
import os
import signal

from benchmark.test_funcs import generate_random_array, monitor_in_separate_process


if __name__ == "__main__":
    main_pid = os.getpid()
    print(f"Main Process ID (PID): {main_pid}")

    monitor_process = multiprocessing.Process(target=monitor_in_separate_process, args=(main_pid,))
    monitor_process.start()

    ### BENCHMARK STARTS HERE ###
    
    arr = generate_random_array(10_000_000) # Replace with the function you want to benchmark
    sorted_arr = arr.copy().sort()
    
    ### BENCHMARK ENDS HERE ###
    os.kill(monitor_process.pid, signal.SIGINT)
    print("Monitor process has been terminated.")  