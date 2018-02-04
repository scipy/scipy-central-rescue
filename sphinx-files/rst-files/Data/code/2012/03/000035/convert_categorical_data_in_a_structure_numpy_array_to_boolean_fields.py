# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

# Author: Warren Weckesser, Enthought, Inc.


import numpy as np


def _to_string(name, join):
    # `name` is either a string, or a tuple of the form (string, value).
    if isinstance(name, tuple):
        s = name[0] + join + str(name[1])
    else:
        s = name
    return s


def bool_fields(a, fields, exclude_fields=None, join='.', bool_dtype=None):
    """
    Convert some fields of a structured array to a group of boolean fields.

    For each field name in `fields`, the unique values in that fields are found,
    and boolean fields are generated in the output array, one field for each
    unique value.

    Parameters
    ----------
    a : numpy structured array
        Array with fields to be converted.
    fields : list of str
        The names of the fields in `a` to be expanded into boolean fields.
    exclude_fields : list of str, optional
        A list of field names that should not be copied to the new array.
        (A field name occurring in `fields` overrides its occurrence in
        `exclude_fields`.)
    join : str, optional
        The string used to create the field names of the new boolean
        fields.  Default is '.'.
    bool_dtype : numpy dtype, optional
        The numpy data type of the "boolean" fields created by this
        function.  Default is `numpy.dtype(numpy.bool)`.

    Return value
    ------------
    b : numpy structured array


    Examples
    --------
    `x` is our sample data:

    >>> dt = np.dtype([('color', 'S10'), ('code', np.int), ('height', np.float64)])
    >>> x = array([('purple', 10, 1.5),
                   ('red', 20, 2.0),
                   ('red', 20, 2.5),
                   ('blue', 10, 1.25),
                   ('purple', 10, 4.0)], dtype=dt)

    Use bool_fields() to expand the categorical data in the `color` and `code`
    fields into separate boolean fields:

    >>> bool_fields(x, fields=['color', 'code'])
    array([(False, True, False, True, False, 1.5),
           (False, False, True, False, True, 2.0),
           (False, False, True, False, True, 2.5),
           (True, False, False, True, False, 1.25),
           (False, True, False, True, False, 4.0)], 
          dtype=[('color.blue', '?'), ('color.purple', '?'), ('color.red', '?'),
                    ('code.10', '?'), ('code.20', '?'), ('height', '<f8')])

    Convert just the `color` field, and use integer values instead of boolean
    in the new fields:

    >>> bool_fields(x, fields=['color'], bool_dtype=np.int8)
    array([(0, 1, 0, 10, 1.5), (0, 0, 1, 20, 2.0), (0, 0, 1, 20, 2.5),
           (1, 0, 0, 10, 1.25), (0, 1, 0, 10, 4.0)], 
          dtype=[('color.blue', 'i1'), ('color.purple', 'i1'), ('color.red', 'i1'),
                 ('code', '<i4'), ('height', '<f8')])

    """
    if bool_dtype is None:
        bool_dtype = np.bool

    if exclude_fields is None:
        exclude_fields = []

    # Create a list that describes the fields of the new array.
    new_field_types = []
    for name in a.dtype.names:
        if name in fields:
            values = np.unique(a[name])
            bin_cols = [((name, value), bool_dtype) for value in values]
            new_field_types.extend(bin_cols)
        elif name not in exclude_fields:
            new_field_types.append((name, a.dtype[name]))

    # dt is the data type of the new array.
    dt = np.dtype([(_to_string(name, join), typ) for name, typ in new_field_types])

    # Allocate the new (empty) array.
    b = np.empty(a.shape, dtype=dt)

    # Fill in the new array.
    for field_name, typ in new_field_types:
        if isinstance(field_name, tuple):
            name, value = field_name
            bin_field_name = _to_string(field_name, join)
            b[bin_field_name] = a[name] == value
        else:
            b[field_name] = a[field_name]
    return b


def pp_struct_array1d(a):
    """" Pretty-print a 1-d structured array.

    This is a "quick and dirty" structured array printer.  It will
    only handle the simplest 1-d structured arrays.
    """
    if a.ndim != 1:
        raise ValueError('Only 1-d structured arrays are handled.')
    names = a.dtype.names
    fw = max(12, max(len(name) for name in names))
    fmt = "%%%ds" % fw
    for name in names:
        print fmt % name,
    print
    for name in names:
        print "-" * fw,
    print
    for row in a:
        for name in names:
            print fmt % row[name],
        print
