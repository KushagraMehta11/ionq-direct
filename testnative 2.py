import pennylane as qml
from pennylane_ionq import ops as ionq_ops
from ionq_direct import SimulatorSubmission
import pennylane_ionq as ionq

# Define a quantum circuit with the specified ansatz using IonQ native gates
def native_ansatz(rots):
    # Set up a quantum device that simulates IonQ's native gates
    dev = ionq.SimulatorDevice(api_key="NpS9onoG5ykjnul619CUaQ1pSx994ARd", wires=3, shots=1000,gateset = "native")

    @qml.qnode(dev)
    def circuit(rots):
        # Apply native GPI gates
        ionq_ops.GPI(rots[0], wires=0)
        ionq_ops.GPI(rots[1], wires=1)
        ionq_ops.GPI(rots[2], wires=2)
        
        # Apply native GPI2 gates
        ionq_ops.GPI2(rots[3], wires=0)
        ionq_ops.GPI2(rots[4], wires=1)
        ionq_ops.GPI2(rots[5], wires=2)
        
        # Apply native MS gate between qubits 0 and 1
        # ionq_ops.MS(rots[6], rots[7], rots[8], wires=[0, 1])
        ionq_ops.MS(rots[6], rots[7], wires=[0, 1])
        # MS gate takes only 2 parameters, as per pennylane_ionq native docs: 
        # https://docs.ionq.com/sdks/pennylane/native-gates-pennylane 


        # Optionally, apply another MS gate between qubits 1 and 2
        # ionq_ops.MS(rots[9], rots[10], rots[11], wires=[1, 2])
        ionq_ops.MS(rots[8], rots[9], wires=[1, 2]) 
        return [qml.expval(qml.PauliZ(i)) for i in range(3)]
    # return qml.state()

    return circuit

# Test function for the SimulatorSubmission class using native gates
def test_native_simulator_submission():
    # Arguments to run the quantum circuit
    rots = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    filename = 'native_test_file.json'
    noise_model = 'aria-1'
    shots = 1000
    api_key = 'YGDYh7Da8ofgZHhYHfJv2TIbHgrrHojV'  # Replace with your actual API key

    # Create a simulator job submission instance
    simulator_job = SimulatorSubmission(qnode=native_ansatz(rots), params=rots, native=True, filename=filename,
                                        api_key=api_key, shots=shots, noise_model=noise_model)

    # # Create the job and print it
    simulator_job.create_job()

    # # Check the IonQ circuit
    print(f"Final IonQ Circuit: {simulator_job.ionq_circuit}")

    # # Save the job to a file
    simulator_job.save_job()

    # print(f"JSON file for job saved to {filename}")

if __name__ == "__main__":
    test_native_simulator_submission()


# import pennylane as qml
# from pennylane_ionq import ops as ionq_ops
# import pennylane_ionq as ionq
# import json
# import requests

# # Define a quantum circuit with specified IonQ native gates
# def native_ansatz(rots):
#     # Set up a quantum device that simulates IonQ's native gates
#     dev = ionq.SimulatorDevice(api_key="YourAPIKey", wires=3, shots=1000, gateset="native")

#     @qml.qnode(dev)
#     def circuit(rots):
#         ionq_ops.GPI(rots[0], wires=0)
#         ionq_ops.GPI(rots[1], wires=1)
#         ionq_ops.GPI(rots[2], wires=2)
#         ionq_ops.GPI2(rots[3], wires=0)
#         ionq_ops.GPI2(rots[4], wires=1)
#         ionq_ops.GPI2(rots[5], wires=2)
#         ionq_ops.MS(rots[6], rots[7], rots[8], wires=[0, 1])
#         ionq_ops.MS(rots[9], rots[10], rots[11], wires=[1, 2])
#         return qml.state()

#     return circuit

# def submit_job(api_key, job_data):
#     url = 'https://api.ionq.co/v0.3/jobs'
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json"
#     }
#     response = requests.post(url, headers=headers, data=json.dumps(job_data))
#     return response.json()

# def test_native_simulator_submission():
#     rots = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
#     api_key = 'YourAPIKey'  # Use your actual API key

#     circuit = native_ansatz(rots)
#     job_data = {
#         "name": "test_native_job",
#         "circuit": circuit.draw(),
#         "shots": 1000,
#         "backend": "simulator",
#         "gateset": "native"
#     }

#     # Submit the job and print the response
#     response = submit_job(api_key, job_data)
#     print("Job submission response:", response)

# if __name__ == "__main__":
#     test_native_simulator_submission()

