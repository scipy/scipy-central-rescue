Convert categorical data in a structure numpy array to boolean fields
=====================================================================

**Author:** warren

**Submitted on:** 2012-03-15 16:58:16-07:00

When analyzing data sets that contain categorical data, it is sometimes necessary to convert a field containing categorical data into separate boolean-valued fields, one field for each possible data value.  The function ``bool_fields`` does this for a NumPy structured array.

Here's a simple example::

    In [31]: dt = np.dtype([('color', 'S10'), ('code', np.int), ('height', np.float64)])
    
    In [32]: x = array([('purple', 10, 1.5),
                        ('red', 20, 2.0),
                        ('red', 20, 2.5),
                        ('blue', 10, 1.25),
                        ('purple', 10, 4.0)], dtype=dt)

|

We'll use ``bool_fields`` to convert the ``color`` and ``code`` fields into boolean fields.  First we import ``bool_fields``, and the simple pretty-printer ``pp_struct_array1d``::

    In [33]: from bool_fields import bool_fields, pp_struct_array1d
    
    In [34]: pp_struct_array1d(x)
           color         code       height
    ------------ ------------ ------------
          purple           10          1.5
             red           20          2.0
             red           20          2.5
            blue           10         1.25
          purple           10          4.0

|

Now we'll convert the ``color`` and ``code`` fields::

    In [35]: b = bool_fields(x, ['color', 'code'])
    
    In [36]: pp_struct_array1d(b)
      color.blue color.purple    color.red      code.10      code.20       height
    ------------ ------------ ------------ ------------ ------------ ------------
           False         True        False         True        False          1.5
           False        False         True        False         True          2.0
           False        False         True        False         True          2.5
            True        False        False         True        False         1.25
           False         True        False         True        False          4.0

|

The ``bool_dtype`` option lets us choose the dtype of the new fields, and the ``exclude_fields`` option lets us remove some fields from the new array.  The ``join`` option lets us set the character that joins the original field name with the unique values to create the new fields names.   For example::

    In [37]: c = bool_fields(x, ['color', 'code'], exclude_fields=['height'], bool_dtype=np.int8, join='_')

    In [38]: pp_struct_array1d(c)
      color_blue color_purple    color_red      code_10      code_20
    ------------ ------------ ------------ ------------ ------------
               0            1            0            1            0
               0            0            1            0            1
               0            0            1            0            1
               1            0            0            1            0
               0            1            0            1            0


.. literalinclude:: /Data/code/2012/03/000035/convert_categorical_data_in_a_structure_numpy_array_to_boolean_fields.py
	:language: python

