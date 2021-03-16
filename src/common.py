import numpy as np
import cirq, sympy


def min_to_vqsd(param_list, num_qubits=2):
    """Helper function that converts a linear array of angles (used to call
    the optimize function) into the format required by VQSD.layer.
    """
    # TODO: add this as a member function of VQSD class
    # error check on input
    assert len(param_list) % 6 == 0, "invalid number of parameters"
    return param_list.reshape(num_qubits // 2, 4, 3)

def vqsd_to_min(param_array):
    """Helper function that converts the array of angles in the format
    required by VQSD.layer into a linear array of angles (used to call the
    optimize function).
    """
    # TODO: add this as a member function of VQSD class
    return param_array.flatten()

def symbol_list(num_qubits, num_layers):
    """Returns a list of sympy.Symbol's for the diagonalizing unitary."""
    return np.array(
        [sympy.Symbol(str(ii)) for ii in range(12 * (num_qubits // 2) * num_layers)]
        )

def symbol_list_for_product(num_qubits):
    """Returns a list of sympy.Symbol's for a product state ansatz."""
    return np.array(
        [sympy.Symbol(str(ii)) for ii in range(num_qubits)]
    )

def get_param_resolver(num_qubits, num_layers):
    """Returns a cirq.ParamResolver for the parameterized unitary."""
    num_angles = 12 * num_qubits * num_layers
    angs = np.pi * (2 * np.random.rand(num_angles) - 1)
    return cirq.ParamResolver(
        {str(ii) : angs[ii] for ii in range(num_angles)}
    )
