# multiprocessing_lib

### Different Solutions

For now we have 1 implemented solution for batch processing with multiple processes:
1. **mp_lock.py:** Each process writes to the same file, and are synched by a multiprocess Lock.

For testing purposes we have the following deprecated solutions:
1. **mp_queue.py:** Uses a single process that is responsible for writing, and the data arives using a Queue.
2. **mp_dist.py:** Each process writes to a different file, and in the end we should join all of them.

### Examples

We have some examples on how to use this lib on examples folder.
- **run_api.py:** calls an API endpoint and save their results on a pickle file.
- **resize_images.py:** resizes a batch of images.

All of the user stdout output from the **process** and **save_callback** functions are redirected to **out_path/user_output.txt**. You can open a new terminal and follow those outputs with:
```sh
tail -f out_path/user_output.txt
```

### Benchmark Options
- **num_procs:** number of processes.
- **result_size:** the result size in KB of every processed element.
- **process_time:** how long should each item should take to process. It is performing some computation, so the CPU is not idle.
- **process_time_jitter:** max variation of process_time.
- **data_size:** how many elements will be processed.
- **save_batch:** joins the results on a batch before saving them to disk.
- **out_path:** where to save the results.

### Running Benchmark

You can generate some benchmark results by running
```sh
python3 run.py
```
The results will be saved on results.txt . Notice that new benchmark runs will append on this file.

### Installing Package

#### Local

```sh
sudo apt install python3-distutils
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
python3 -m pip install build
python3 -m build
python3 -m pip install dist/doc_ock-0.0.1-py3-none-any.whl --force-reinstall
```

Knwon bugs with Python3.9, so beware.
