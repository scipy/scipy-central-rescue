f2py with opaque Fortran derived types
======================================

**Author:** pv

**Submitted on:** 2013-02-04 02:16:14-08:00

f2py does not natively (as of Jan 2013) directly support Fortran derived types. However, you can trick it to treat them as opaque blobs, as shown here, if you tell it how many bytes it should reserve. The exact number of bytes required may vary with compiler/compiler options, so it should be chosen big enough.


.. literalinclude:: /Data/code/2013/02/000060/f2py_with_opaque_fortran_derived_types.py
	:language: python

