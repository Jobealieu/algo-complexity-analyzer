import time
import matplotlib
# Remove the non-GUI backend to allow popup windows
# matplotlib.use('Agg')  # Commented out to enable graph popup
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

class AlgorithmAnalyzer:
    """Analyzes time complexity of various algorithms"""
    
    @staticmethod
    def bubble_sort(arr):
        """Bubble sort implementation - O(n²)"""
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    @staticmethod
    def linear_search(arr, target):
        """Linear search implementation - O(n)"""
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return -1
    
    @staticmethod
    def binary_search(arr, target):
        """Binary search implementation - O(log n)"""
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return -1
    
    @staticmethod
    def nested_loop(n):
        """Nested loop - O(n²)"""
        count = 0
        for i in range(n):
            for j in range(n):
                count += 1
        return count
    
    @staticmethod
    def exponential_algo(n):
        """Exponential algorithm - O(2^n) - limited to small n"""
        if n <= 1:
            return n
        return AlgorithmAnalyzer.exponential_algo(n - 1) + AlgorithmAnalyzer.exponential_algo(n - 2)
    
    @staticmethod
    def get_complexity(algo_name):
        """Returns the time complexity notation for each algorithm"""
        complexities = {
            "bubble": "O(n²)",
            "linear": "O(n)",
            "binary": "O(log n)",
            "nested": "O(n²)",
            "exponential": "O(2^n)"
        }
        return complexities.get(algo_name, "O(n)")
    
    @staticmethod
    def analyze_algorithm(algo_name, max_n, steps):
        """
        Analyzes an algorithm's performance across different input sizes
        
        Args:
            algo_name: Name of algorithm to analyze
            max_n: Maximum number of elements
            steps: Number of steps to divide the range into
        
        Returns:
            Dictionary with analysis results including graph as base64
        """
        start_time = time.time() * 1000  # Convert to milliseconds
        
        # Generate input sizes
        n_values = np.linspace(10, max_n, steps, dtype=int)
        times = []
        
        # Measure execution time for each input size
        for n in n_values:
            if algo_name == "bubble":
                arr = list(range(n, 0, -1))  # Worst case: reversed array
                algo_start = time.perf_counter()
                AlgorithmAnalyzer.bubble_sort(arr.copy())
                algo_end = time.perf_counter()
                
            elif algo_name == "linear":
                arr = list(range(n))
                target = n - 1  # Worst case: last element
                algo_start = time.perf_counter()
                AlgorithmAnalyzer.linear_search(arr, target)
                algo_end = time.perf_counter()
                
            elif algo_name == "binary":
                arr = list(range(n))
                target = n - 1
                algo_start = time.perf_counter()
                AlgorithmAnalyzer.binary_search(arr, target)
                algo_end = time.perf_counter()
                
            elif algo_name == "nested":
                algo_start = time.perf_counter()
                AlgorithmAnalyzer.nested_loop(n)
                algo_end = time.perf_counter()
                
            elif algo_name == "exponential":
                # Limit exponential to small values to avoid infinite runtime
                n_limited = min(n, 30)
                algo_start = time.perf_counter()
                AlgorithmAnalyzer.exponential_algo(n_limited)
                algo_end = time.perf_counter()
            else:
                raise ValueError(f"Unknown algorithm: {algo_name}")
            
            times.append((algo_end - algo_start) * 1000)  # Convert to ms
        
        # Generate graph
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, times, marker='o', linestyle='-', linewidth=2, markersize=6)
        plt.xlabel('Input Size (n)', fontsize=12)
        plt.ylabel('Execution Time (ms)', fontsize=12)
        plt.title(f'{algo_name.title()} Sort - Time Complexity: {AlgorithmAnalyzer.get_complexity(algo_name)}', 
                  fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Show the graph in a popup window
        plt.show()  # THIS MAKES IT POP UP!
        
        # Also save as base64 for API response
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()
        
        end_time = time.time() * 1000
        total_time = end_time - start_time
        
        return {
            "algo": algo_name,
            "items": max_n,
            "steps": steps,
            "start_time": start_time,
            "end_time": end_time,
            "total_time_ms": round(total_time, 2),
            "time_complexity": AlgorithmAnalyzer.get_complexity(algo_name),
            "path_to_graph": image_base64
        }
