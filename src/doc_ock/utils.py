import types
import pickle
import contextlib
import os


class InvalidArgumentsError(Exception):
    """Exception raised when passing invalid arguments."""

    def __init__(self, argument, expected_value):
        message = f'Invalid {argument}. Expected values: {expected_value}'
        super().__init__(message)


def validate_inputs(data_list, process, save_callback, num_procs, out_path, save_batch, batch_size=1):
    if isinstance(data_list, list)==False or len(data_list) == 0:
        raise InvalidArgumentsError('data_list', 'list(str) > 0')
    if isinstance(process, types.FunctionType) == False:
        raise InvalidArgumentsError('process', 'function')
    if isinstance(num_procs, int) == False or num_procs <= 0:
        raise InvalidArgumentsError('num_procs', 'int > 0')
    if isinstance(out_path, str) == False or len(out_path) == 0:
        raise InvalidArgumentsError('out_path', 'len(str) > 0')
    if isinstance(save_batch, int) == False or save_batch <= 0:
        raise InvalidArgumentsError('save_batch', 'int > 0')
    if isinstance(batch_size, int) == False or batch_size <= 0:
        raise InvalidArgumentsError('batch_size', 'int > 0')


def save_results(output_filepath, data_results, data_names):
    pkl_filepath = f'{os.path.splitext(output_filepath)[0]}_tmp.pkl'
    with open(pkl_filepath, 'ab+') as fid:
        pickle.dump({'data_name': data_names, 'results': data_results}, fid)


def load_results(data_list, output_path):
    pkl_filepath = os.path.join(output_path, 'data_tmp.pkl')
    results = {'data_name': [], 'results': []}
    with open(pkl_filepath, 'rb') as fid:
        with contextlib.suppress(EOFError):
            data = pickle.load(fid)
            while data is not None:
                results['data_name'].extend(data['data_name'])
                results['results'].extend(data['results'])
                data = pickle.load(fid)

    # messy code to reorder results based on data_list input
    data_order_map = {x: idx for idx,x in enumerate(data_list)}
    order = [data_order_map[x] for x in results['data_name']]
    combined_data = [(x,y) for x,y in zip(results['results'], order)]
    ordered_results = sorted(combined_data, key=lambda x: x[1])

    return [x[0] for x in ordered_results]
