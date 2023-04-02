import qiskit as qk
from qiskit import QuantumCircuit, Aer, IBMQ
from qiskit import transpile, assemble, execute
from qiskit.visualization import plot_histogram
from qiskit import transpile
from qiskit.extensions import UnitaryGate
from qiskit.circuit.library.standard_gates import RXGate
from qiskit.circuit.library import CXGate
from qiskit.dagcircuit import DAGOpNode
from qiskit.converters import circuit_to_dag, dag_to_circuit

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import copy
import math
from sklearn.cluster import KMeans

np.random.seed(123)

def grayvalue_to_angle(value, pi_frac=1):
    return value * pi/pi_frac

def grayscale_to_angles(image_mat, pi_frac=1):
    for i in range(len(image_mat)):
        for j in range(len(image_mat)):
            image_mat[i][j] = grayvalue_to_angle(image_mat[i][j], pi_frac)
    
    return image_mat

def generate_random_image(row=8, col=8):
    return np.random.rand(row, col)

def QIE_V1(image, get_depth=False):
    image_angles = copy.deepcopy(image)
    image_angles = grayscale_to_angles(image_angles)
    
    max_intensity = max([val for row in image for val in row])
    
    intensities = [i for image_row in image for i in image_row]
    sqrt_intensities = [np.sqrt(i) for i in intensities]
    scaled_intensities = [i*(1/np.sqrt(sum(intensities))) for i in sqrt_intensities]
    
    qc = QuantumCircuit(6)
    # initialization to match amplitudes
    qc.initialize(scaled_intensities)
    qc.measure_all()
    
    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, shots=2**15).result()
    counts = result.get_counts(qc)

    highest_count = max(counts.values())
    rec_image = [[0 for _ in range(8)] for _ in range(8)]

    for k in counts.keys():
        q1 = int(k[:3], 2)
        q2 = int(k[3:], 2)

        rec_image[q1][q2] = (counts[k]/highest_count)*max_intensity
        
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    _ = ax1.imshow(image, cmap='gray', vmin=0, vmax=1)
    _ = ax1.set_title('Original Image')

    _ = ax2.imshow(rec_image, cmap='gray', vmin=0, vmax=1)
    _ = ax2.set_title('Reconstructed Image')
    
    image_diff = image - rec_image
    squared_diff = 0
    for i in range(len(image_diff)):
        for j in range(len(image_diff[i])):
            squared_diff += image_diff[i][j]**2

    fig.suptitle(f'\nReconstruction Squared Error:\n{squared_diff}')
    plt.show()
    if get_depth:
        return transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3).depth()
    
    
def QIE_V1_1(image, get_depth=False):
    image_angles = copy.deepcopy(image)
    image_angles = grayscale_to_angles(image_angles, 4)
    
    max_intensity = max([val for row in image for val in row])
    
    intensities = [i for image_row in image for i in image_row]
    sqrt_intensities = [np.sqrt(i) for i in intensities]
    scaled_intensities = [i*(1/np.sqrt(sum(intensities))) for i in sqrt_intensities]
    
    qc_aux = QuantumCircuit(6)
    qc_aux.initialize(scaled_intensities)
    transpiled_circuit = transpile(qc_aux, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3)

    backend = Aer.get_backend('unitary_simulator')
    job = execute(transpiled_circuit, backend, shots=2**15)
    initial_state = UnitaryGate(job.result().get_unitary(qc_aux))
    
    theta = grayvalue_to_angle(max_intensity, 4)

    qc = QuantumCircuit(7)

    qc.append(initial_state, [i for i in range(6)])
    qc.rx(theta, 6)
    qc.measure_all()

    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, shots=2**15).result()
    counts = result.get_counts(qc)

    rec_image = [[0 for _ in range(8)] for _ in range(8)]

    pos_counts = {k[1:]:0 for k in counts.keys()}
    max_intensity_counter = [0, 0]
    for k in counts.keys():
        pos_counts[k[1:]] += counts[k]
        max_intensity_counter[int(k[0])] += counts[k]

    highest_count = max(pos_counts.values())
    max_intensity = max_intensity_counter[0]/sum(max_intensity_counter)
    for k in pos_counts.keys():
        q1 = int(k[:3], 2)
        q2 = int(k[3:], 2)

        rec_image[q1][q2] = (pos_counts[k]/highest_count)*max_intensity
        
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    _ = ax1.imshow(image, cmap='gray', vmin=0, vmax=1)
    _ = ax1.set_title('Original Image')

    _ = ax2.imshow(rec_image, cmap='gray', vmin=0, vmax=1)
    _ = ax2.set_title('Reconstructed Image')
    
    image_diff = image - rec_image
    squared_diff = 0
    for i in range(len(image_diff)):
        for j in range(len(image_diff[i])):
            squared_diff += image_diff[i][j]**2

    fig.suptitle(f'\nReconstruction Squared Error:\n{squared_diff}')
    plt.show()
    
    if get_depth:
        return transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3).depth()
    
def QIE_V2(image, get_depth=False):
    image_angles = copy.deepcopy(image)
    image_angles = grayscale_to_angles(image_angles)
    
    max_intensity = max([val for row in image for val in row])
    
    intensities = [i for image_row in image for i in image_row]
    sqrt_intensities = [np.sqrt(i) for i in intensities]
    scaled_intensities = [i*(1/np.sqrt(sum(intensities))) for i in sqrt_intensities]
    
    qc = QuantumCircuit(7)

    qc.h([i for i in range(6)])
    for i in range(len(image_angles)):
        for j in range(len(image_angles[i])):
            theta = image_angles[i][j]

            pos = i*len(image_angles) + j
            bin_pos = str(bin(pos))[2:]
            bin_pos = '0'*(6-len(bin_pos)) + bin_pos
            bin_pos = [int(i) for i in bin_pos]

            filter_low = []
            for k in range(len(bin_pos)):
                if bin_pos[k] == 0:
                    filter_low.append(k)
                    qc.x(k)

            qc.mcrx(theta, [i for i in range(6)], 6)
            if len(filter_low) > 0:
                qc.x(filter_low)

    qc.measure_all()
    
    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    qobj = assemble(t_qc, shots=2**15)
    result = aer_sim.run(qobj).result()
    counts = result.get_counts(qc)
    
    rec_image_components = [[[0, 0] for _ in range(8)] for _ in range(8)]
    highest_count = max(counts.values())

    for k in counts.keys():
        color = k[0]
        qubit = k[1:][::-1]
        pos = int(qubit, 2)
        row = math.floor(pos / len(image))
        col = pos % len(image[row])
        rec_image_components[row][col][int(color)] = counts[k]
        
    rec_image = [[0 for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if sum(rec_image_components[i][j]) > 0:
                rec_image[i][j] = rec_image_components[i][j][1]/sum(rec_image_components[i][j])
                
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    _ = ax1.imshow(image, cmap='gray', vmin=0, vmax=1)
    _ = ax1.set_title('Original Image')

    _ = ax2.imshow(rec_image, cmap='gray', vmin=0, vmax=1)
    _ = ax2.set_title('Reconstructed Image')
    
    image_diff = image - rec_image
    squared_diff = 0
    for i in range(len(image_diff)):
        for j in range(len(image_diff[i])):
            squared_diff += image_diff[i][j]**2

    fig.suptitle(f'\nReconstruction Squared Error:\n{squared_diff}')
    plt.show()
    
    if get_depth:
        return transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3).depth()
    
def QIE_V3(image, get_depth=False):
    image_angles = copy.deepcopy(image)
    image_angles = grayscale_to_angles(image_angles)
    
    max_intensity = max([val for row in image for val in row])
    
    intensities = np.array([[value] for image_row in image for value in image_row])
    positions_map = [[] for _ in range(int((len(image)/2)**2))]
    avg_intensities = [0 for _ in range(int((len(image)/2)**2))]

    kmeans = KMeans(n_clusters=int((len(image)/2)**2), random_state=0).fit(intensities)

    for i,val in enumerate(kmeans.labels_):
        avg_intensities[val] += intensities[i][0]
        positions_map[val].append(i)

    for i in range(len(avg_intensities)):
        if list(kmeans.labels_).count(i) > 0:
            avg_intensities[i] = avg_intensities[i] / list(kmeans.labels_).count(i)
            
    image_4 = np.array(avg_intensities).reshape((4, 4))
    
    intensities = [i for image_row in image_4 for i in image_row]
    sqrt_intensities = [np.sqrt(i) for i in avg_intensities]
    scaled_intensities = [i*(1/np.sqrt(sum(avg_intensities))) for i in sqrt_intensities]
    
    qc = QuantumCircuit(4)
    qc.initialize(scaled_intensities)
    qc.measure_all()
    
    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, shots=2**15).result()
    counts = result.get_counts(qc)
                               
    highest_count = max(counts.values())
    rec_image = [[0 for _ in range(4)] for _ in range(4)]

    for k in counts.keys():
        q1 = int(k[:2], 2)
        q2 = int(k[2:], 2)

        rec_image[q1][q2] = (counts[k]/highest_count)*max_intensity
                               
    final_rec_image = [[0 for _ in range(len(image))] for _ in range(len(image))]
    vec_intensities = [val for row in rec_image for val in row]

    for i,val in enumerate(vec_intensities):
        for k in range(len(positions_map[i])):
            pos_x = math.floor(positions_map[i][k]/len(image))
            pos_y = positions_map[i][k]%len(image)
            final_rec_image[pos_x][pos_y] = val
                               
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    _ = ax1.imshow(image, cmap='gray', vmin=0, vmax=1)
    _ = ax1.set_title('Original Image')

    _ = ax2.imshow(final_rec_image, cmap='gray', vmin=0, vmax=1)
    _ = ax2.set_title('Reconstructed Image')
    
    image_diff = image - final_rec_image
    squared_diff = 0
    for i in range(len(image_diff)):
        for j in range(len(image_diff[i])):
            squared_diff += image_diff[i][j]**2

    fig.suptitle(f'\nReconstruction Squared Error:\n{squared_diff}')
    plt.show()
    
    if get_depth:
        return transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3).depth()
    
def QIE_V3_1(image, get_depth=False):
    image_angles = copy.deepcopy(image)
    image_angles = grayscale_to_angles(image_angles)
    
    max_intensity = max([val for row in image for val in row])
    
    intensities = np.array([[value] for image_row in image for value in image_row])
    positions_map = [[] for _ in range(int((len(image)/2)**2))]
    avg_intensities = [0 for _ in range(int((len(image)/2)**2))]

    kmeans = KMeans(n_clusters=int((len(image)/2)**2), random_state=0).fit(intensities)

    for i,val in enumerate(kmeans.labels_):
        avg_intensities[val] += intensities[i][0]
        positions_map[val].append(i)

    for i in range(len(avg_intensities)):
        if list(kmeans.labels_).count(i) > 0:
            avg_intensities[i] = avg_intensities[i] / list(kmeans.labels_).count(i)
            
    image_4 = np.array(avg_intensities).reshape((8, 8))
    
    intensities = [i for image_row in image_4 for i in image_row]
    sqrt_intensities = [np.sqrt(i) for i in avg_intensities]
    scaled_intensities = [i*(1/np.sqrt(sum(avg_intensities))) for i in sqrt_intensities]
    
    qc = QuantumCircuit(6)
    qc.initialize(scaled_intensities)
    qc.measure_all()
    
    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, shots=2**15).result()
    counts = result.get_counts(qc)
                               
    highest_count = max(counts.values())
    rec_image = [[0 for _ in range(8)] for _ in range(8)]

    for k in counts.keys():
        q1 = int(k[:3], 2)
        q2 = int(k[3:], 2)

        rec_image[q1][q2] = (counts[k]/highest_count)*max_intensity
                               
    final_rec_image = [[0 for _ in range(len(image))] for _ in range(len(image))]
    vec_intensities = [val for row in rec_image for val in row]

    for i,val in enumerate(vec_intensities):
        for k in range(len(positions_map[i])):
            pos_x = math.floor(positions_map[i][k]/len(image))
            pos_y = positions_map[i][k]%len(image)
            final_rec_image[pos_x][pos_y] = val
                               
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    _ = ax1.imshow(image, cmap='gray', vmin=0, vmax=1)
    _ = ax1.set_title('Original Image')

    _ = ax2.imshow(final_rec_image, cmap='gray', vmin=0, vmax=1)
    _ = ax2.set_title('Reconstructed Image')
    
    image_diff = image - final_rec_image
    squared_diff = 0
    for i in range(len(image_diff)):
        for j in range(len(image_diff[i])):
            squared_diff += image_diff[i][j]**2

    fig.suptitle(f'\nReconstruction Squared Error:\n{squared_diff}')
    plt.show()
    
    if get_depth:
        return transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3).depth()
    
def QIE_V4(image, get_depth=False):
    image_angles = copy.deepcopy(image)
    image_angles = grayscale_to_angles(image_angles)
    
    max_intensity = max([val for row in image for val in row])
    
    intensities = []

    for i in range(len(image)):
        for j in range(len(image[i])):
            intensities.append((image[i][j], i, j))

    intensities = sorted(intensities)

    avg_intensities = [0 for _ in range(len(intensities))]
    positions_map = []

    i = 0
    for j in range(4):
        for i in range(4):
            i*=2
            i+= 16*j
            avg_intensities[i:i+2] = np.ones(2)*(intensities[i][0] + intensities[i+1][0] + intensities[i+2][0] + intensities[i+3][0]) / 4.0
            avg_intensities[i+8:i+10] = np.ones(2)*(intensities[i][0] + intensities[i+1][0] + intensities[i+2][0] + intensities[i+3][0]) / 4.0
            positions_map.append([intensities[i][1]*len(image)+intensities[i][2], intensities[i+1][1]*len(image)+intensities[i+1][2], intensities[i+8][1]*len(image)+intensities[i+8][2], intensities[i+9][1]*len(image)+intensities[i+9][2]])
    image_8 = np.array(avg_intensities).reshape((8, 8))
    
    intensities = [i for image_row in image_8 for i in image_row]
    sqrt_intensities = [np.sqrt(i) for i in avg_intensities]
    scaled_intensities = [i*(1/np.sqrt(sum(avg_intensities))) for i in sqrt_intensities]
    
    qc = QuantumCircuit(6)
    qc.initialize(scaled_intensities)
    qc.measure_all()

    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, shots=2**15).result()
    counts = result.get_counts(qc)
    
    highest_count = max(counts.values())
    rec_image = [[0 for _ in range(8)] for _ in range(8)]

    for k in counts.keys():
        q1 = int(k[:3], 2)
        q2 = int(k[3:], 2)

        rec_image[q1][q2] = (counts[k]/highest_count)*max_intensity

    final_rec_image = [[0 for _ in range(len(image))] for _ in range(len(image))]
    vec_intensities = [val for row in rec_image for val in row]
    for i in range(math.floor(len(vec_intensities)/4)):
        for k in range(4):
            pos_x = math.floor(positions_map[i][k]/len(image))
            pos_y = positions_map[i][k]%len(image)

            if i % 8 >= 4:
                z = 8
            else:
                z = 0

            if k <2:
                vec_index = 2*i + k
            else:
                vec_index = 2*i + 8 + k - 2

            index_x = 2 * (i//4) + k//2 + 2*(i // 16)
            index_y = (2*i) % 8 + k % 2
            final_rec_image[pos_x][pos_y] = rec_image[index_x][index_y]
    
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    _ = ax1.imshow(image, cmap='gray', vmin=0, vmax=1)
    _ = ax1.set_title('Original Image')

    _ = ax2.imshow(final_rec_image, cmap='gray', vmin=0, vmax=1)
    _ = ax2.set_title('Reconstructed Image')
    
    image_diff = image - final_rec_image
    squared_diff = 0
    for i in range(len(image_diff)):
        for j in range(len(image_diff[i])):
            squared_diff += image_diff[i][j]**2

    fig.suptitle(f'\nReconstruction Squared Error:\n{squared_diff}')
    plt.show()
    
    if get_depth:
        return transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3).depth()

def theoretical_best_image_generator(get_depth=False):
    qc = QuantumCircuit(6)

    # Randomize thetas
    min_theta = 0
    max_theta = 2
    thetas = ((max_theta - min_theta) * np.random.rand((6)) + min_theta) * np.pi
    
    # Calculate the coeficients
    alphas = np.zeros((6, 2), dtype="complex")
    alphas[:, 0] = np.cos(thetas/2).transpose()
    alphas[:, 1] = -1j * np.sin(thetas/2).transpose()

    # Create the image the thetas represent
    image = np.zeros((8, 8), dtype="float")
    for index in range(64):
        ones = np.array(list(map(int, list(f"{str(bin(index))[2:]:0>6}"[::-1]))))
        prod = 1
        for j in range(6):
            prod *= alphas[j, ones[j]]

        # Store the intensity
        image[index//8][index % 8] = abs(prod**2)
    maxi = max([val for row in image for val in row])

    max_intensity = 1
    for i in range(8):
        for j in range(8):
            image[j][i] = (image[j][i] / maxi) * max_intensity


    for index, th in enumerate(thetas):
        qc.rx(th, index)
    qc.measure_all()
    
    qc = QuantumCircuit(6)
    qubits = [0, 1, 2, 3, 4, 5]

    qc.sx(qubits)
    for th, qu in zip(thetas, qubits):
        qc.rz(th - np.pi, qu)
    qc.sx(qubits)
    qc.measure_all()
    
    aer_sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(qc, aer_sim)
    result = aer_sim.run(t_qc, shots=2**15).result()
    counts = result.get_counts(qc)
    
    highest_count = max(counts.values())
    rec_image = [[0 for _ in range(8)] for _ in range(8)]

    for k in counts.keys():
        q1 = int(k[:3], 2)
        q2 = int(k[3:], 2)

        rec_image[q1][q2] = (counts[k]/highest_count)*max_intensity
        
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    _ = ax1.imshow(image, cmap='gray', vmin=0, vmax=1)
    _ = ax1.set_title('Original Image')

    _ = ax2.imshow(rec_image, cmap='gray', vmin=0, vmax=1)
    _ = ax2.set_title('Reconstructed Image')
    
    image_diff = image - rec_image
    squared_diff = 0
    for i in range(len(image_diff)):
        for j in range(len(image_diff[i])):
            squared_diff += image_diff[i][j]**2

    fig.suptitle(f'\nReconstruction Squared Error:\n{squared_diff}')
    plt.show()
    
    if get_depth:
        return transpile(qc, basis_gates=['cx', 'id', 'rz', 'sx', 'x'], optimization_level=3).depth()