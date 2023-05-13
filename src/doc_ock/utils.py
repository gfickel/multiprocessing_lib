import types


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