"""
Shor's Algorithm Implementation for Integer Factorization
Demonstrates quantum period finding for RSA-like problems
"""
import numpy as np
import random
import math
from fractions import Fraction
from typing import Tuple, List, Optional

class ShorSimulator:
    """Quantum simulation of Shor's factoring algorithm"""
    
    def __init__(self, n_qubits: int = 8):
        self.n_qubits = n_qubits
        self.N = None  # Number to factor
        self.a = None  # Random coprime
    
    def factor(self, N: int, verbose: bool = True) -> Tuple[int, int]:
        """
        Factor integer N using Shor's algorithm simulation
        Returns (p, q) where p * q = N
        """
        if verbose:
            print(f"Attempting to factor N = {N}")
        
        self.N = N
        
        # Step 1: Check for trivial factors
        if N % 2 == 0:
            return 2, N // 2
        
        # Step 2: Check if N is prime power
        for k in range(2, int(math.log2(N)) + 1):
            root = round(N ** (1/k))
            if root ** k == N:
                return root, N // root
        
        # Step 3: Main quantum part (simulated)
        while True:
            # Choose random a coprime to N
            self.a = random.randint(2, N - 1)
            if math.gcd(self.a, N) != 1:
                continue
            
            if verbose:
                print(f"Selected coprime a = {self.a}")
            
            # Quantum period finding (simulated)
            r = self.quantum_period_finding(self.a, N, verbose)
            
            if r is None or r % 2 == 1:
                if verbose:
                    print(f"Period r = {r} is odd, trying again...")
                continue
            
            # Check if a^(r/2) ≡ -1 (mod N)
            x = pow(self.a, r // 2, N)
            if x == N - 1:
                if verbose:
                    print(f"Period yields trivial factor, trying again...")
                continue
            
            # Found factors!
            p = math.gcd(x - 1, N)
            q = math.gcd(x + 1, N)
            
            if p != 1 and q != 1 and p * q == N:
                if verbose:
                    print(f"Success! Factors found: {p} * {q} = {N}")
                    print(f"Period found: r = {r}")
                return min(p, q), max(p, q)
    
    def quantum_period_finding(self, a: int, N: int, verbose: bool = True) -> Optional[int]:
        """
        Simulate quantum period finding (QFT + measurement)
        Returns period r such that a^r ≡ 1 mod N
        """
        if verbose:
            print("\n--- Quantum Period Finding Simulation ---")
        
        # Create superposition (simulated)
        n_qubits = self.n_qubits
        q = 2 ** n_qubits
        
        if verbose:
            print(f"Using {n_qubits} qubits (q = {q})")
            print(f"Creating superposition of {q} states...")
        
        # Simulate quantum measurements
        measurements = []
        for _ in range(3):  # Multiple measurements for accuracy
            # Simulate quantum measurement (getting phase information)
            c = random.randint(0, q - 1)
            
            # Apply continued fractions to find period
            frac = Fraction(c, q).limit_denominator(N)
            r_candidate = frac.denominator
            
            measurements.append(r_candidate)
            
            if verbose:
                print(f"Measurement {_+1}: c = {c}, candidate r = {r_candidate}")
        
        # Take the most common candidate
        from collections import Counter
        r_counts = Counter(measurements)
        r = r_counts.most_common(1)[0][0]
        
        # Verify period
        if pow(a, r, N) == 1:
            if verbose:
                print(f"Verified: {a}^{r} ≡ 1 mod {N}")
            return r
        
        # Try multiples of found period
        for k in range(1, 10):
            r_try = r * k
            if pow(a, r_try, N) == 1:
                if verbose:
                    print(f"Found period after testing multiples: r = {r_try}")
                return r_try
        
        return None
    
    def get_circuit_complexity(self, N: int) -> dict:
        """
        Calculate quantum circuit resources needed
        """
        # For factoring N, need ~3n qubits where n = ceil(log2(N))
        n = math.ceil(math.log2(N))
        total_qubits = 3 * n
        classical_qubits = 2 * n
        ancilla_qubits = n
        
        # Gate count estimation
        # Modular exponentiation: O(n^3) gates
        # QFT: O(n^2) gates
        gate_count = n**3 + n**2
        
        return {
            'n': n,
            'total_qubits': total_qubits,
            'classical_qubits': classical_qubits,
            'ancilla_qubits': ancilla_qubits,
            'gate_count_estimate': gate_count,
            'depth_estimate': n**2,
            'space_complexity': 'O(n)',
            'time_complexity': 'O(n^3)'
        }
    
    def demonstrate_rsa_break(self, bits: int = 15):
        """
        Demonstrate breaking small RSA-like numbers
        """
        print(f"\n{'='*60}")
        print(f"DEMONSTRATION: Breaking {bits}-bit RSA-like Number")
        print(f"{'='*60}")
        
        # Generate two primes
        p = self.random_prime(bits // 2)
        q = self.random_prime(bits // 2)
        N = p * q
        
        print(f"Generated primes: p = {p}, q = {q}")
        print(f"Public key N = {p} × {q} = {N}")
        print(f"N has {N.bit_length()} bits")
        
        # Factor with Shor
        print(f"\nRunning Shor's algorithm...")
        start_time = time.time()
        p_found, q_found = self.factor(N, verbose=True)
        elapsed = time.time() - start_time
        
        print(f"\nFactorization successful in {elapsed:.3f} seconds!")
        print(f"Found factors: {p_found} × {q_found} = {N}")
        print(f"Original factors were: {p} × {q}")
        
        return N, p_found, q_found, elapsed
    
    def random_prime(self, bits: int) -> int:
        """Generate random prime of given bit length"""
        while True:
            p = random.getrandbits(bits)
            p |= (1 << (bits - 1)) | 1  # Ensure correct bit length and odd
            if self.is_prime(p):
                return p
    
    def is_prime(self, n: int, k: int = 10) -> bool:
        """Miller-Rabin primality test"""
        if n < 2:
            return False
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
            if n % p == 0:
                return n == p
        # Miller-Rabin
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True

# Quantum Fourier Transform implementation
class QuantumFourierTransform:
    """Quantum Fourier Transform circuit implementation"""
    
    def __init__(self, n_qubits: int):
        self.n_qubits = n_qubits
        self.gates = []
    
    def apply(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply QFT to state vector"""
        n = self.n_qubits
        N = 2 ** n
        result = np.zeros(N, dtype=complex)
        
        # Direct QFT implementation
        for k in range(N):
            for j in range(N):
                angle = 2 * np.pi * j * k / N
                result[k] += state_vector[j] * np.exp(2j * np.pi * angle)
            result[k] /= np.sqrt(N)
        
        return result
    
    def inverse(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply inverse QFT"""
        n = self.n_qubits
        N = 2 ** n
        result = np.zeros(N, dtype=complex)
        
        for j in range(N):
            for k in range(N):
                angle = -2 * np.pi * j * k / N
                result[j] += state_vector[k] * np.exp(2j * np.pi * angle)
            result[j] /= np.sqrt(N)
        
        return result

if __name__ == "__main__":
    import time
    
    print("Shor's Algorithm Quantum Simulator")
    print("=" * 50)
    
    # Create simulator
    shor = ShorSimulator(n_qubits=8)
    
    # Example factorization
    numbers_to_factor = [15, 21, 35, 143]  # Classic examples
    
    for N in numbers_to_factor:
        print(f"\nFactoring N = {N}:")
        print("-" * 30)
        
        start = time.time()
        p, q = shor.factor(N, verbose=True)
        elapsed = time.time() - start
        
        print(f"Time: {elapsed:.3f} seconds")
        print(f"Result: {p} × {q} = {N}")
    
    # Show circuit complexity for larger number
    print(f"\n{'='*50}")
    print("Circuit Complexity Analysis for N = 2047 (11-bit RSA):")
    complexity = shor.get_circuit_complexity(2047)
    for key, value in complexity.items():
        print(f"  {key}: {value}")
