"""
Shor's Algorithm Implementation for Integer Factorization
Demonstrates quantum period finding for RSA-like problems
"""
import numpy as np
import random
import math
import time
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
        attempts = 0
        max_attempts = 10
        
        while attempts < max_attempts:
            attempts += 1
            
            # Choose random a coprime to N
            self.a = random.randint(2, N - 1)
            if math.gcd(self.a, N) != 1:
                if verbose:
                    print(f"Attempt {attempts}: a = {self.a} (not coprime, skipping)")
                continue
            
            if verbose:
                print(f"\nAttempt {attempts}:")
                print(f"  Random coprime a = {self.a}")
                print(f"  gcd({self.a}, {N}) = 1 ✓")
            
            # Quantum period finding (simulated)
            r = self.quantum_period_finding(self.a, N, verbose)
            
            if r is None:
                if verbose:
                    print(f"  Could not find period, trying again...")
                continue
            
            if r % 2 == 1:
                if verbose:
                    print(f"  Period r = {r} is odd, trying again...")
                continue
            
            # Check if a^(r/2) ≡ -1 (mod N)
            x = pow(self.a, r // 2, N)
            if x == N - 1:
                if verbose:
                    print(f"  a^(r/2) = {x} gives trivial factor, trying again...")
                continue
            
            # Found factors!
            p = math.gcd(x - 1, N)
            q = math.gcd(x + 1, N)
            
            if p != 1 and q != 1 and p * q == N:
                if verbose:
                    print(f"\n✅ SUCCESS on attempt {attempts}!")
                    print(f"  Period found: r = {r}")
                    print(f"  Factors: {p} × {q} = {N}")
                
                return min(p, q), max(p, q)
            else:
                if verbose:
                    print(f"  Found invalid factors: {p}, {q}")
        
        raise RuntimeError(f"Failed to factor {N} after {max_attempts} attempts")
    
    def quantum_period_finding(self, a: int, N: int, verbose: bool = True) -> Optional[int]:
        """
        Simulate quantum period finding (QFT + measurement)
        Returns period r such that a^r ≡ 1 mod N
        """
        if verbose:
            print("  --- Quantum Period Finding ---")
        
        n_qubits = self.n_qubits
        q = 2 ** n_qubits
        
        # Simulate multiple quantum measurements
        measurements = []
        
        for shot in range(3):  # Multiple quantum measurements
            # Simulate quantum measurement outcome
            c = random.randint(0, q - 1)
            
            # Use continued fractions to find period candidates
            frac = Fraction(c, q).limit_denominator(N)
            r_candidate = frac.denominator
            
            measurements.append(r_candidate)
            
            if verbose:
                print(f"  Measurement {shot+1}: c = {c}, candidate r = {r_candidate}")
        
        # Find most common candidate
        from collections import Counter
        if measurements:
            r_counts = Counter(measurements)
            r = r_counts.most_common(1)[0][0]
            
            # Verify period
            if pow(a, r, N) == 1:
                if verbose:
                    print(f"  Verified: {a}^{r} ≡ 1 mod {N}")
                return r
        
        # Try to find period by testing multiples
        if verbose:
            print("  Testing potential periods...")
        
        # Test potential periods up to a reasonable limit
        max_test = min(1000, N)
        for r in range(1, max_test):
            if pow(a, r, N) == 1:
                if verbose:
                    print(f"  Found period by testing: r = {r}")
                return r
        
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

class QuantumFourierTransform:
    """Quantum Fourier Transform circuit implementation"""
    
    def __init__(self, n_qubits: int):
        self.n_qubits = n_qubits
        self.gates = []
    
    def apply(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply QFT to state vector"""
        n = self.n_qubits
        N = 2 ** n
        
        # Direct QFT implementation using DFT matrix
        omega = np.exp(2j * np.pi / N)
        dft_matrix = np.array([[omega**(j*k) for k in range(N)] for j in range(N)]) / np.sqrt(N)
        
        return dft_matrix @ state_vector
    
    def inverse(self, state_vector: np.ndarray) -> np.ndarray:
        """Apply inverse QFT"""
        n = self.n_qubits
        N = 2 ** n
        
        # Inverse DFT matrix
        omega = np.exp(-2j * np.pi / N)  # Note: negative sign for inverse
        idft_matrix = np.array([[omega**(j*k) for k in range(N)] for j in range(N)]) / np.sqrt(N)
        
        return idft_matrix @ state_vector

# Simple test when run directly
if __name__ == "__main__":
    print("Shor's Algorithm Quantum Simulator")
    print("=" * 50)
    
    # Create simulator
    shor = ShorSimulator(n_qubits=8)
    
    # Test factorization
    test_numbers = [15, 21]
    
    for N in test_numbers:
        print(f"\nFactoring N = {N}:")
        try:
            p, q = shor.factor(N, verbose=True)
            print(f"Result: {p} × {q} = {N}")
            print(f"Verification: {p} * {q} = {p * q}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test QFT
    print(f"\n{'='*50}")
    print("Quantum Fourier Transform Test")
    qft = QuantumFourierTransform(3)
    test_state = np.array([1, 0, 0, 0, 0, 0, 0, 0], dtype=complex)
    result = qft.apply(test_state)
    print(f"QFT of |000⟩: {np.abs(result)**2}")
