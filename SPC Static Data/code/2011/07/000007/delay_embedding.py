# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0

import numpy as np

def embed(array, dim, lag=1):
    """Create a delay embedding of array given a resulting dimension and lag.
    The array will be raveled before embedding.
    """
    array = np.asarray(array)
    array = array.ravel()
    new = np.lib.stride_tricks.as_strided(array,
                                         (len(array)-dim*lag+lag, dim),
                                         (array.itemsize, array.itemsize*lag))
    return new