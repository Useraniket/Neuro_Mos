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
            lambda x: x[0] & x[1] & x[2] & x[3] & x[4] & x[5] & x[6])
    
    def perform_majority1(self, input_seq):
        """Majority function for 7 inputs (output is 1 if 2 or more inputs are 1)"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if sum(x) >= 2 else 0)

    def perform_majority2(self, input_seq):
        """Majority function for 7 inputs (output is 1 if 3 or more inputs are 1)"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if sum(x) >= 3 else 0)

    def perform_majority3(self, input_seq):
        """Majority function for 7 inputs (output is 1 if 4 or more inputs are 1)"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if sum(x) >= 4 else 0)

    def perform_diff_logic_1(self, input_seq):
        """Logic function: ABCDE + ABCDF + ABCDG + ABCEF + ABCEG + ABCFG + ABDEF + ABDEG + ABDFG + ABEFG +
                         ACDEF + ACDEG + ACDFG + ACEFG + ADEFG + BCDEF + BCDEG + BCDFG + BCEFG + BDEFG + CDEFG"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if (
                # ABCDE
                (x[0] & x[1] & x[2] & x[3] & x[4]) or
                # ABCDF
                (x[0] & x[1] & x[2] & x[3] & x[5]) or
                # ABCDG
                (x[0] & x[1] & x[2] & x[3] & x[6]) or
                # ABCEF
                (x[0] & x[1] & x[2] & x[4] & x[5]) or
                # ABCEG
                (x[0] & x[1] & x[2] & x[4] & x[6]) or
                # ABCFG
                (x[0] & x[1] & x[2] & x[5] & x[6]) or
                # ABDEF
                (x[0] & x[1] & x[3] & x[4] & x[5]) or
                # ABDEG
                (x[0] & x[1] & x[3] & x[4] & x[6]) or
                # ABDFG
                (x[0] & x[1] & x[3] & x[5] & x[6]) or
                # ABEFG
                (x[0] & x[1] & x[4] & x[5] & x[6]) or
                # ACDEF
                (x[0] & x[2] & x[3] & x[4] & x[5]) or
                # ACDEG
                (x[0] & x[2] & x[3] & x[4] & x[6]) or
                # ACDFG
                (x[0] & x[2] & x[3] & x[5] & x[6]) or
                # ACEFG
                (x[0] & x[2] & x[4] & x[5] & x[6]) or
                # ADEFG
                (x[0] & x[3] & x[4] & x[5] & x[6]) or
                # BCDEF
                (x[1] & x[2] & x[3] & x[4] & x[5]) or
                # BCDEG
                (x[1] & x[2] & x[3] & x[4] & x[6]) or
                # BCDFG
                (x[1] & x[2] & x[3] & x[5] & x[6]) or
                # BCEFG
                (x[1] & x[2] & x[4] & x[5] & x[6]) or
                # BDEFG
                (x[1] & x[3] & x[4] & x[5] & x[6]) or
                # CDEFG
                (x[2] & x[3] & x[4] & x[5] & x[6])
            ) else 0)
        
    def perform_diff_logic_2(self, input_seq):
        """Logic function: ABCDEF + ABCDEG + ABCDFG + ABCEFG + ABDEFG + ACDEFG + BCDEFG"""
        self.perform_gate_operation(input_seq, 
            lambda x: 1 if (
                # ABCDEF
                (x[0] & x[1] & x[2] & x[3] & x[4] & x[5]) or
                # ABCDEG
                (x[0] & x[1] & x[2] & x[3] & x[4] & x[6]) or
                # ABCDFG
                (x[0] & x[1] & x[2] & x[3] & x[5] & x[6]) or
                # ABCEFG
                (x[0] & x[1] & x[2] & x[4] & x[5] & x[6]) or
                # ABDEFG
                (x[0] & x[1] & x[3] & x[4] & x[5] & x[6]) or
                # ACDEFG
                (x[0] & x[2] & x[3] & x[4] & x[5] & x[6]) or
                # BCDEFG
                (x[1] & x[2] & x[3] & x[4] & x[5] & x[6])
            ) else 0)
            
    def perform_or(self, input_seq):
        self.perform_gate_operation(input_seq, 
            lambda x: x[0] | x[1] | x[2] | x[3] | x[4] | x[5] | x[6])
    
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
        plt.title(f'{gate_type} Gate Output Response (7-input)')
        plt.ylim(-0.1, self.vdd + 0.1)
        plt.show()

def generate_7_input_sequences():
    """Generate all possible 7-bit input combinations"""
    sequences = []
    for i in range(128):  # 2^7 = 128 possible combinations
        # Convert number to 7-bit binary and pad with zeros
        binary = format(i, '07b')
        # Convert string bits to integers
        sequence = [int(bit) for bit in binary]
        sequences.append(sequence)
    return sequences

def main():
    try:
        # Get threshold voltage from user
        Vth = float(input('Enter threshold voltage (0-1.8V): '))
        
        # Generate all possible 7-input sequences
        input_seq = generate_7_input_sequences()
        
        # Initialize simulator
        simulator = GateSimulator()
        gate_type = ""
        
       # Select operation based on threshold voltage - keeping original thresholds
        if 0 < Vth < 0.254:
            simulator.perform_or(input_seq)
            gate_type = "OR"
        elif 0.254 <= Vth < 0.511:
            simulator.perform_majority1(input_seq)
            gate_type = "MAJORITY1"      
        elif 0.511 <= Vth < 0.767:
            simulator.perform_majority2(input_seq)
            gate_type = "MAJORITY2"
        elif 0.767 <= Vth < 1.023:
            simulator.perform_majority3(input_seq)
            gate_type = "MAJORITY3"          
        elif 1.023 <= Vth < 1.279:
            simulator.perform_diff_logic_1(input_seq)
            gate_type = "DIFFERENT-LOGIC:1"  #ABCDE + ABCDF + ABCDG + ABCEF + ABCEG + ABCFG + ABDEF + ABDEG + ABDFG + ABEFG +
                                             #ACDEF + ACDEG + ACDFG + ACEFG + ADEFG + BCDEF + BCDEG + BCDFG + BCEFG + BDEFG + CDEFG
        elif 1.279 <= Vth < 1.535:
            simulator.perform_diff_logic_2(input_seq)
            gate_type = "DIFFERENT-LOGIC:2"  #ABCDEF + ABCDEG + ABCDFG + ABCEFG + ABDEFG + ACDEFG + BCDEFG 
        elif 1.535 <= Vth <= 1.8:
            simulator.perform_and(input_seq)
            gate_type = "AND"
        else:
            print("Invalid threshold voltage. Please enter a value between 0 and 1.8V")
            return
            
        # Save results to file
        simulator.save_results(f"{gate_type.lower()}_gate_data.txt")
        
        # Print results
        print(f"\n{gate_type} Gate Simulation Results (7-input):")
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