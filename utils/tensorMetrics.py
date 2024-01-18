import numpy as np

def unique_to_matrix(tensor):
    """
    Function to convert a FSL-like tensor image (with the unique values) to
    a true DTI matrix.
    :param tensor: FSL-like tensor image.
    :return:
    """
    # Vector representation of the matrix for each unique value.
    # This vectorization is based on how FSL defines the DTI image (tensor).
    tensor_vec = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1],
    ])
    tensor = np.expand_dims(tensor, -1)
    tensor_vec = np.expand_dims(tensor_vec, (0, 1, 2))
    tensor_vectorized = np.sum(tensor * tensor_vec, -2)
    matrix_shape = tensor_vectorized.shape[:-1] + (3, 3)
    return np.reshape(tensor_vectorized, matrix_shape)

def get_dti_metrics(tensor):
    """
    Function to get the QUaD22 DTI metrics based on an FSL-like tensor
    image.
    :param tensor: FSL-like tensor image.
    :return:
    """
    # Initial preprocessing to obtain the eignevalues of the tensor.
    # It seems that float16 is the prefered type to replicate FA as closely
    # as possible to the FSL image. The small cascaded errors seem to lead to
    # a large MSE difference.
    dti_matrix = unique_to_matrix(tensor.astype(np.float16))
    v = np.real(np.linalg.eigvals(dti_matrix))

    num_sq12 = (v[..., 0] - v[..., 1]) ** 2
    num_sq13 = (v[..., 0] - v[..., 2]) ** 2
    num_sq23 = (v[..., 1] - v[..., 2]) ** 2
    fa_num = num_sq12 + num_sq13 + num_sq23
    fa_den = np.sum(v ** 2, axis=-1)
    fa_den[fa_den == 0] = 1e-5

    fa = np.sqrt(0.5 * fa_num / fa_den)
    md = np.sum(v, axis=-1) / 3
    ad = np.sort(v, axis=-1)[..., -1]
    rd = (np.sort(v, axis=-1)[..., 0] + np.sort(v, axis=-1)[..., 1])/2

    return fa, md, ad, rd