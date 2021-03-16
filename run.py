from src.VQSD import VQSD, symbol_list_for_product
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np
import time, cirq

n = 8               # Number of qubits
QOBJS = []          # Weighted sum of local and global cost

def qcost(angs, nreps=500, q=0.5):
    # PDIP cost
    vqsd.clear_dip_test_circ()
    pdip = vqsd.obj_pdip_resolved(angs, repetitions=nreps)
    
    # DIP cost
    vqsd.clear_dip_test_circ()
    vqsd.dip_test()
    dip = vqsd.obj_dip_resolved(angs, repetitions=nreps)
    
    # weighted sum
    obj = q * dip + (1 - q) * pdip
    
    QOBJS.append(obj)
    print("QCOST OBJ =", obj)
    
    return obj


def plot(data):
    with plt.style.context('ggplot'):
        plt.plot(data, "r-o", linewidth=2, label="q = 0.5")
        plt.xlabel("Iteration", fontsize=15, fontweight="bold")
        plt.ylabel("Cost", fontsize=15, fontweight="bold")
        plt.savefig("q=0.5_" + time.asctime() + ".pdf", format="pdf")


if __name__ == "__main__":    

    # Get a VQSD instance
    vqsd = VQSD(n)
    
    # Get preparation angles
    sprep_angles = np.random.rand(n)
    
    # Add the state prep circuit, compute the purity, add ansatz
    vqsd.product_state_prep(sprep_angles, cirq.rx)
    vqsd.compute_purity()
    vqsd.product_ansatz(symbol_list_for_product(n), cirq.rx)
    
    # Minimize using the weighted cost
    weight = minimize(qcost, np.zeros(n), method="COBYLA", options={"maxiter": 1000})

    plot(QOBJS)
