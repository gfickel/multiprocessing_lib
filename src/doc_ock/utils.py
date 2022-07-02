import types


class InvalidArgumentsError(Exception):
    """Exception raised when passing invalid arguments."""

    def __init__(self, argument, expected_value):
        message = f'Invalid {argument}. Expected values: {expected_value}'
        super().__init__(message)


def validate_inputs(data_list, process, save_callback, num_procs, out_path, save_batch):
    if not isinstance(data_list, list) or len(data_list) == 0:
        raise InvalidArgumentsError('data_list', 'list(str) > 0')
    if not isinstance(process, (types.FunctionType, types.MethodType)):
        raise InvalidArgumentsError('process', 'function')
    if not isinstance(num_procs, int) or num_procs <= 0:
        raise InvalidArgumentsError('num_procs', 'int > 0')
    if not isinstance(out_path, str) or len(out_path) == 0:
        raise InvalidArgumentsError('out_path', 'len(str) > 0')
    if not isinstance(save_batch, int) or save_batch <= 0:
        raise InvalidArgumentsError('save_batch', 'int > 0')
