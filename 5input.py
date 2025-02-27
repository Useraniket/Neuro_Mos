import time
import math
import matplotlib.pyplot as plt

class GateSimulator:
    def __init__(self, vdd=1.8):
        self.vdd = vdd
        self.results = []
        self.time_start = time.time()
        
    def dac(self, digital):
        """Convert digital input to analog voltage"""
        return digital * self.vdd
    
    def get_elapsed_time(self):
        """Get current elapsed time in seconds, rounded to 3 decimal places"""
        return round(time.time() - self.time_start, 3)
    
    def add_transition_point(self, current_time, from_value, to_value):
        """Add a transition point slightly before the actual change"""
        transition_time = round(current_time - 0.001, 3)
        self.results.append([transition_time, from_value])
        self.results.append([current_time, to_value])
    
    def perform_gate_operation(self, input_seq, operation):
        """Perform the specified gate operation on input sequences"""
        prev_output = None
        
        for sequence in input_seq:
            current_time = self.get_elapsed_time()
            output = self.dac(operation(sequence))
            
            if prev_output is not None and prev_output != output:
                # Add transition point
                self.add_transition_point(current_time, prev_output, output)
            else:
                self.results.append([current_time, output])
                
            prev_output = output
            time.sleep(0.01)
    
    def perform_and(self, input_seq):
        self.perform_gate_operation(input_seq, 
            lambda x: x[0] & x[1] & x[2] & x[3] & x[4])
    
    def perform_majority(self, input_seq):
        """Majority function for 5 inputs (output is 1 if 3 or more inputs are 1)"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if sum(x) >= 3 else 0)
    
    def perform_diff_logic_1(self, input_seq):
        """Logic function: (A + B + C) · (A + B + D + E) · (C + D + E)"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if ((x[0] | x[1] | x[2]) and 
                           (x[0] | x[1] | x[3] | x[4]) and 
                           (x[2] | x[3] | x[4])) else 0)
        
    def perform_diff_logic_2(self, input_seq):
        """Logic function: ABCD + ABCE + ABDE + ACDE + BCDE"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if ((x[0] & x[1] & x[2] & x[3]) or 
                           (x[0] & x[1] & x[2] & x[4]) or 
                           (x[0] & x[1] & x[3] & x[4]) or 
                           (x[0] & x[2] & x[3] & x[4]) or 
                           (x[1] & x[2] & x[3] & x[4])) else 0)
            
    def perform_or(self, input_seq):
        self.perform_gate_operation(input_seq, 
            lambda x: x[0] | x[1] | x[2] | x[3] | x[4])
    
    def save_results(self, filename):
        """Save results to a file"""
        with open(filename, "w") as file:
            for time_point, voltage in self.results:
                file.write(f"{time_point}, {voltage}\n")
    
    def plot_results(self, gate_type):
        """Plot the voltage vs time graph"""
        times, voltages = zip(*self.results)
        
        plt.figure(figsize=(12, 6))
        plt.plot(times, voltages, 'b-', linewidth=2)
        plt.grid(True)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.title(f'{gate_type} Gate Output Response (5-input)')
        plt.ylim(-0.1, self.vdd + 0.1)
        plt.show()

def generate_5_input_sequences():
    """Generate all possible 5-bit input combinations"""
    sequences = []
    for i in range(32):  # 2^5 = 32 possible combinations
        # Convert number to 5-bit binary and pad with zeros
        binary = format(i, '05b')
        # Convert string bits to integers
        sequence = [int(bit) for bit in binary]
        sequences.append(sequence)
    return sequences

def main():
    try:
        # Get threshold voltage from user
        Vth = float(input('Enter threshold voltage (0-1.8V): '))
        
        # Generate all possible 5-input sequences
        input_seq = generate_5_input_sequences()
        
        # Initialize simulator
        simulator = GateSimulator()
        gate_type = ""
        
        # Select operation based on threshold voltage - keeping original thresholds
        if 0 < Vth < 0.36:
            simulator.perform_or(input_seq)
            gate_type = "OR"
        elif 0.36 <= Vth < 0.72:
            simulator.perform_diff_logic_1(input_seq)
            gate_type = "DIFFERENT-LOGIC:1"  #(A + B + C) · (A + B + D + E) · (C + D + E)
        elif 0.72 <= Vth < 1.08:
            simulator.perform_majority(input_seq)
            gate_type = "MAJORITY"  #ABC + ABD + ABE + ACD + ACE + ADE + BCD + BCE + BDE + CDE
        elif 1.08 <= Vth < 1.44:
            simulator.perform_diff_logic_2(input_seq)
            gate_type = "DIFFERENT-LOGIC:2"  #ABCD + ABCE + ABDE + ACDE + BCDE 
        elif 1.44 <= Vth < 1.8:
            simulator.perform_and(input_seq)
            gate_type = "AND"
        else:
            print("Invalid threshold voltage. Please enter a value between 0 and 1.8V")
            return
        
        # Save results to file
        simulator.save_results(f"{gate_type.lower().replace(' ', '_').replace(':','_')}_gate_data.txt")
        
        # Print results
        print(f"\n{gate_type} Gate Simulation Results (5-input):")
        print("Time (s) | Voltage (V)")
        print("-" * 30)
        for time_point, voltage in simulator.results:
            print(f"{time_point:8.3f} | {voltage:8.2f}")
        
        # Plot results
        simulator.plot_results(gate_type)
        
    except ValueError:
        print("Please enter a valid number for the threshold voltage")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()