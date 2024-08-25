import pennylane as qml
from ionq_direct import SimulatorSubmission
import pennylane_ionq as ionq

# Define a quantum circuit with the specified ansatz using standard gates
def ansatz(rots):
    # Set up a quantum device with IonQ
    dev = ionq.SimulatorDevice(api_key="YGDYh7Da8ofgZHhYHfJv2TIbHgrrHojV", wires=3, gateset="qis")

    @qml.qnode(dev)
    def circuit(rots):
        # Apply Hadamard gates to each qubit
        qml.Hadamard(wires=0)
        qml.Hadamard(wires=1)
        qml.Hadamard(wires=2)
        
        # Apply Pauli-X rotations with parameters
        qml.RX(rots[0], wires=0)
        qml.RX(rots[1], wires=1)
        qml.RX(rots[2], wires=2)
        
        # Apply Pauli-Y rotations with parameters
        qml.RY(rots[3], wires=0)
        qml.RY(rots[4], wires=1)
        qml.RY(rots[5], wires=2)
        
        # Apply Pauli-Z rotations with parameters
        qml.RZ(rots[6], wires=0)
        qml.RZ(rots[7], wires=1)
        qml.RZ(rots[8], wires=2)
        
        # Measure the expectation values of PauliZ on each qubit
        return [qml.expval(qml.PauliZ(i)) for i in range(3)]

    return circuit

# Test function for the SimulatorSubmission class
def test_simulator_submission():
    # Arguments to run the quantum circuit
    rots = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    filename = 'test_file.json'
    noise_model = 'aria-1'
    shots = 1000
    api_key = 'YGDYh7Da8ofgZHhYHfJv2TIbHgrrHojV'  # Replace with your actual API key

    # Create a simulator job submission instance
    simulator_job = SimulatorSubmission(qnode=ansatz(rots), params=rots, native=False, filename=filename,
                                        api_key=api_key, shots=shots, noise_model=noise_model)

    # Create the job and print it
    simulator_job.create_job()

    # Check the IonQ circuit
    print(f"Final IonQ Circuit: {simulator_job.ionq_circuit}")

    # Save the job to a file
    simulator_job.save_job()

    print(f"JSON file for job saved to {filename}")

if __name__ == "__main__":
    test_simulator_submission()
    # Uncomment the following line to test QPU submission
    # test_qpu_submission()

