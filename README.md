# multiprocessing_lib

### What does it do?

It helps us create code that easily use multiple CPU cores, especially long computations that produce intermediate results. Another important feature is the ability to resume a previous computation after it stopped, either by a crash or user interference.

### How to use it?

You must model your problem with the following pieces:
* **process_function(data_sample, shared_data, init_values)**: a processing function that executes a single piece of data and possibly returns a value
* **data_list**: a list of data to be processed. Can be a list of images to be resized, inputs to different probabilistic models, or wathever you want. But it must be represented as str.
* **def save_callback(output_filepath, data_results, data_names)**: a save callback that receives the output file path (without extension), a list of results and their respective data_samples . This function is guaranteed to be thread safe.

The save_callback is not required, but often is quite useful. For example, we have an example that calls a Rest API and save the results on a pickle object. Another common usage of mine is to resize images, and in this case the new image is directly being saved inside process_function, so no save_callback is necessary.

So the main idea is that you must have a list of (str) data to be processed, create a function that process a single one of them, and possibly define a callback to save intermediate results. Notice that this lib will keep track of processed data even if no save_callback is provided, so if the process is interupted, you can resume from where it stopped.

An example on how this would look like:
```py
    data_list = [str(i) for i in range(10)]
    shared_data = {
        'some_data': 42,
        'big_model_path': 'path.bin',
    }
    def my_init(shared_data):
        ml_model = load_model(shared_data['big_model_path'])
        return {'model': ml_model}

    def process(data, shared_data={}, init_values={}):
        my_model = init_values['model']
        res = my_model.process(data)
        print(res, shared_data['some_data'])

    mp_lock(data_list, process, None, 4, "dummy_output", shared_data=shared_data, init_function=my_init)
```
The **mp_lock** function is the one that does the magic. Notice this None, that would be where our save_callback would be if we wanted one and returned some value to be saved from process. We also are passing 4 as the number of processes to use, and providing an output path. This is required, since it will be where some internal stuff will be saved on disk, and where the save_callback results will be saved.

We also are using **shared_data** and **init_function** options, that will be discussed in the following section.

## Interesting Options

The **process_function** provides two variables, usually dict, that can be used for some interesting options. A quick explanation:
* **shared_data**: data that will be available within all concurrent process_function . Usefull to share some configurations, or wathever you want. Notice that this variable should be used as a Read Only, since modifications will not reflect on the process_function that are running on different processes.
* **init_values**: values that came from an **init_function** that you may pass when using this lib. This function will be called once on every process, despite the number of times that process_function will be called. This is good to initialize some heavy stuff that you don't want to be doing on every process_function call, and/or the values cannot be pickled. My common use case is to instantiate a Machine Learning model that usually cannot be pickled and are slow to load.

You can also use **mp_lock_values** that returns the list of the results returned by your process_function. Usefull when you want get the values right on Python and keep up with your code, instead of loading the results from the output path.

### Installing Package
Add the following line to your requirements.txt
```
git+https://github.com/gfickel/multiprocessing_lib
```
Or manually run the following:
```
python3 -m pip install git+https://github.com/gfickel/multiprocessing_lib
```
