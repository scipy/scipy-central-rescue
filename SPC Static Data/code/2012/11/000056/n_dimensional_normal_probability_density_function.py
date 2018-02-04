# License: Creative Commons Zero (almost public domain) http://scpyce.org/cc0
""" N-dimensional normal PDFs
"""
import numpy as np
from numpy import sqrt, pi, exp

def npdf_1d(x, mu = 0, sigma2 = 1):
    """ 1D normal PDF for input vector `x`, given mean `mu`, variance `sigma2`

    http://en.wikipedia.org/wiki/Normal_distribution

    .. math::

        f(x;\mu,\sigma^2) = \frac{1}{\sigma\sqrt{2\pi}} e^{ -\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2 }

    Parameters
    ----------
    x : scalar or length N vector
        If scalar, value at which to evaluate PDF.  If vector, vector of values
        at which to evaluate PDF
    mu : scalar, optional
        mean for normal distribution
    sigma2 : scalar, optional
        variance of normal distribution (:math:`sigma^2`)

    Returns
    -------
    pdf_vals : scalar or length N vector
        If `x` was a scalar, return scalar value for PDF.  If `x`
        was vector length N, return length N vector giving values for each of
        specified N points.
    """
    mu = np.float64(mu)
    sigma2 = np.float64(sigma2)
    return 1. / sqrt(sigma2 * 2 * pi) * exp(-((x - mu)**2 / sigma2) / 2)


def npdf_nd(x, mu = 0, sigma2 = 1):
    """ ND normal PDF, given mean vector `mu` and covariance matrix `sigma2`

    http://en.wikipedia.org/wiki/Multivariate_normal_distribution#Density_function

    .. math::

        f_{\mathbf x}(x_1,\ldots,x_k)\, =
        \frac{1}{(2\pi)^{k/2}|\boldsymbol\Sigma|^{1/2}}
        \exp\left(-\frac{1}{2}({\mathbf x}-{\boldsymbol\mu})^T{\boldsymbol\Sigma}^{-1}({\mathbf x}-{\boldsymbol\mu})
        \right)

    where :math:`\left|\boldsymbol\Sigma\right|` is the determinant of
    :math:`\boldsymbol\Sigma`

    Parameters
    ----------
    x : scalar or length D vector or shape (D, N) array
        If vector, length of vector is dimension of PDF.  If 2D array then ``D``
        is dimension of PDF and ``N`` is number of samples.
    mu : scalar or length D vector
        means for normal distribution for each dimension of PDF.  If scalar,
        mean is the same for each dimension
    sigma2 : scalar or length D vector or (D, D) array
        If scalar, gives variance for all D dimensions of PDF.  If vector, gives
        diagonal of covariance matrix (one variance for each dimension,
        dimensions are independent).  If (D, D) array gives full covariance
        matrix for dimensions of PDF.

    Returns
    -------
    pdf_vals : scalar or length N vector
        If `x` was a scalar or a vector, return scalar value for PDF.  If `x`
        was shape (D, N) return length N vector giving values for each of
        specified N points.
    """
    x = np.array(x)
    if x.ndim == 1: # dimension of normal is length of row axis
        x = x[:, None]
    if x.ndim == 0:
        k = 1
    else:
        k, _ = x.shape
    mu = np.array(mu)
    if mu.ndim == 1:
        mu = mu[:, None]
    x_mu = x - mu
    sigma2 = np.array(sigma2)
    # Use shortcuts for simple sigma2s
    if sigma2.size == 1: # sigma2 is scalar
        isigma2_x_mu = x_mu / sigma2
        sigma2_det = sigma2 ** k
    elif sigma2.ndim == 1: # sigma2 is the diagonal
        isigma2_x_mu = x_mu / sigma2[:, None]
        sigma2_det = np.prod(sigma2)
    else: # sigma2 is covariance matrix
        isigma2_x_mu = np.dot(np.linalg.inv(sigma2), x_mu)
        sigma2_det = np.linalg.det(sigma2)
    # Formula above does not apply to matrices but to vectors
    to_exp = -1. / 2 * np.sum(x_mu * isigma2_x_mu, axis=0)
    front = (2 * np.pi) ** (-k / 2.) / np.sqrt(sigma2_det)
    return front * np.exp(to_exp)


def test_pdf():
    # Test values from:
    # repr(ssd.norm(0, 1).pdf(np.linspace(-5, 5, 100)))
    from numpy.testing import assert_array_almost_equal
    x = np.linspace(-5, 5, 100)
    # Test values from:
    # repr(ssd.norm(0, 1).pdf(np.linspace(-5, 5, 100)))
    exp_vals_0_1 = np.array([1.48671951e-06,   2.45106104e-06,   3.99989037e-06,
                             6.46116639e-06,   1.03310066e-05,   1.63509589e-05,
                             2.56160812e-05,   3.97238224e-05,   6.09759040e-05,
                             9.26476353e-05,   1.39341123e-04,   2.07440309e-04,
                             3.05686225e-04,   4.45889725e-04,   6.43795498e-04,
                             9.20104770e-04,   1.30165384e-03,   1.82273110e-03,
                             2.52649578e-03,   3.46643792e-03,   4.70779076e-03,
                             6.32877643e-03,   8.42153448e-03,   1.10925548e-02,
                             1.44624148e-02,   1.86646099e-02,   2.38432745e-02,
                             3.01496139e-02,   3.77369231e-02,   4.67541424e-02,
                             5.73380051e-02,   6.96039584e-02,   8.36361772e-02,
                             9.94771388e-02,   1.17117360e-01,   1.36486009e-01,
                             1.57443188e-01,   1.79774665e-01,   2.03189836e-01,
                             2.27323506e-01,   2.51741947e-01,   2.75953371e-01,
                             2.99422683e-01,   3.21590023e-01,   3.41892294e-01,
                             3.59786558e-01,   3.74773979e-01,   3.86422853e-01,
                             3.94389234e-01,   3.98433802e-01,   3.98433802e-01,
                             3.94389234e-01,   3.86422853e-01,   3.74773979e-01,
                             3.59786558e-01,   3.41892294e-01,   3.21590023e-01,
                             2.99422683e-01,   2.75953371e-01,   2.51741947e-01,
                             2.27323506e-01,   2.03189836e-01,   1.79774665e-01,
                             1.57443188e-01,   1.36486009e-01,   1.17117360e-01,
                             9.94771388e-02,   8.36361772e-02,   6.96039584e-02,
                             5.73380051e-02,   4.67541424e-02,   3.77369231e-02,
                             3.01496139e-02,   2.38432745e-02,   1.86646099e-02,
                             1.44624148e-02,   1.10925548e-02,   8.42153448e-03,
                             6.32877643e-03,   4.70779076e-03,   3.46643792e-03,
                             2.52649578e-03,   1.82273110e-03,   1.30165384e-03,
                             9.20104770e-04,   6.43795498e-04,   4.45889725e-04,
                             3.05686225e-04,   2.07440309e-04,   1.39341123e-04,
                             9.26476353e-05,   6.09759040e-05,   3.97238224e-05,
                             2.56160812e-05,   1.63509589e-05,   1.03310066e-05,
                             6.46116639e-06,   3.99989037e-06,   2.45106104e-06,
                             1.48671951e-06])
    # repr(ssd.norm(-2.1, 1.3).pdf(np.linspace(-5, 5, 100)))
    exp_vals_off = np.array([2.54900148e-02,   3.02228751e-02,   3.56188176e-02,
                             4.17254715e-02,   4.85848695e-02,   5.62313954e-02,
                             6.46896370e-02,   7.39722112e-02,   8.40776415e-02,
                             9.49883782e-02,   1.06669058e-01,   1.19065099e-01,
                             1.32101737e-01,   1.45683583e-01,   1.59694784e-01,
                             1.73999853e-01,   1.88445194e-01,   2.02861337e-01,
                             2.17065865e-01,   2.30866976e-01,   2.44067600e-01,
                             2.56469946e-01,   2.67880353e-01,   2.78114272e-01,
                             2.87001208e-01,   2.94389425e-01,   3.00150257e-01,
                             3.04181829e-01,   3.06412054e-01,   3.06800780e-01,
                             3.05340988e-01,   3.02059003e-01,   2.97013710e-01,
                             2.90294791e-01,   2.82020073e-01,   2.72332098e-01,
                             2.61394037e-01,   2.49385129e-01,   2.36495817e-01,
                             2.22922758e-01,   2.08863900e-01,   1.94513788e-01,
                             1.80059249e-01,   1.65675584e-01,   1.51523369e-01,
                             1.37745925e-01,   1.24467491e-01,   1.11792107e-01,
                             9.98031807e-02,   8.85636804e-02,   7.81168932e-02,
                             6.84876559e-02,   5.96839661e-02,   5.16988735e-02,
                             4.45125546e-02,   3.80944748e-02,   3.24055574e-02,
                             2.74002820e-02,   2.30286566e-02,   1.92380127e-02,
                             1.59745946e-02,   1.31849205e-02,   1.08169100e-02,
                             8.82077924e-03,   7.14971486e-03,   5.76034538e-03,
                             4.61303085e-03,   3.67199623e-03,   2.90533441e-03,
                             2.28490455e-03,   1.78615041e-03,   1.38786118e-03,
                             1.07189455e-03,   8.22879282e-04,   6.27911196e-04,
                             4.76253696e-04,   3.59051317e-04,   2.69062221e-04,
                             2.00413491e-04,   1.48381316e-04,   1.09196700e-04,
                             7.98762827e-05,   5.80770046e-05,   4.19728641e-05,
                             3.01516466e-05,   2.15293787e-05,   1.52802335e-05,
                             1.07796962e-05,   7.55894320e-06,   5.26858118e-06,
                             3.65009614e-06,   2.51358146e-06,   1.72051973e-06,
                             1.17058885e-06,   7.91638932e-07,   5.32142489e-07,
                             3.55554977e-07,   2.36136771e-07,   1.55882913e-07,
                             1.02284879e-07])
    assert_array_almost_equal(npdf_1d(x), exp_vals_0_1)
    assert_array_almost_equal(npdf_1d(x, 0), exp_vals_0_1)
    assert_array_almost_equal(npdf_1d(x, 0, 1), exp_vals_0_1)
    assert_array_almost_equal(npdf_1d(x, -2.1, 1.3**2), exp_vals_off)
    for x0, v in zip(x, exp_vals_0_1):
        assert_array_almost_equal(npdf_1d(x0, 0, 1), v)
    for x0, v in zip(x, exp_vals_off):
        assert_array_almost_equal(npdf_1d(x0, -2.1, 1.3**2), v)
    # ND should equal 1D
    xv = x[None, :] # points vector, 1D normal
    assert_array_almost_equal(npdf_nd(xv), exp_vals_0_1)
    assert_array_almost_equal(npdf_nd(xv, 0), exp_vals_0_1)
    assert_array_almost_equal(npdf_nd(xv, 0, 1), exp_vals_0_1)
    assert_array_almost_equal(npdf_nd(xv, -2.1, 1.3**2), exp_vals_off)
    # sigma2 shortcuts
    assert_array_almost_equal(npdf_nd(xv, -2.1, [1.3**2]), exp_vals_off)
    xa = np.row_stack((x, x))
    assert_array_almost_equal(npdf_nd(xa, -2.1, 1.3**2),
                              npdf_nd(xa, -2.1, [1.3 ** 2]))
    assert_array_almost_equal(npdf_nd(xa, -2.1, 1.3**2),
                              npdf_nd(xa, -2.1, [1.3**2] * 2))
    assert_array_almost_equal(npdf_nd(xa, -2.1, 1.3**2),
                              npdf_nd(xa, -2.1, np.eye(2) * 1.3**2))
