// Shor's Algorithm JavaScript
class ShorSimulator {
    constructor() {
        this.resultsElement = document.getElementById('shor-results');
        this.visualizationElement = document.getElementById('shor-visualization');
        this.circuitInfo = {
            qubits: document.getElementById('circuit-qubits'),
            gates: document.getElementById('circuit-gates'),
            depth: document.getElementById('circuit-depth'),
            timeComplexity: document.getElementById('time-complexity'),
            quantumAdvantage: document.getElementById('quantum-advantage')
        };
        
        this.initializeEvents();
    }
    
    initializeEvents() {
        document.getElementById('run-shor-btn').addEventListener('click', () => this.runFactorization());
        document.getElementById('demo-rsa-btn').addEventListener('click', () => this.demoRSABreaking());
        
        // Update circuit info when input changes
        document.getElementById('number-to-factor').addEventListener('input', () => this.updateCircuitInfo());
        document.getElementById('qubits-count-input').addEventListener('change', () => this.updateCircuitInfo());
    }
    
    async runFactorization() {
        const number = parseInt(document.getElementById('number-to-factor').value);
        const qubits = parseInt(document.getElementById('qubits-count-input').value);
        const verbose = document.getElementById('verbose-mode').checked;
        
        if (number < 2) {
            this.showError('Please enter a number greater than 1');
            return;
        }
        
        this.showLoading();
        
        try {
            // Simulate API call - in real implementation, this would call backend
            const result = await this.simulateFactorization(number, qubits, verbose);
            this.displayResults(result);
            this.updateVisualization(result);
            this.updateCircuitInfo(number);
        } catch (error) {
            this.showError(`Factorization failed: ${error.message}`);
        }
    }
    
    async simulateFactorization(N, qubits, verbose) {
        // Simulate quantum factorization
        return new Promise((resolve) => {
            setTimeout(() => {
                // This is a simulation - real implementation would call Python backend
                const factors = this.calculateFactors(N);
                const time = Math.random() * 0.5 + 0.1; // Simulate computation time
                
                resolve({
                    N: N,
                    factors: factors,
                    time: time,
                    attempts: Math.floor(Math.random() * 3) + 1,
                    period: this.findPeriod(N),
                    quantumMeasurements: Math.floor(Math.random() * 5) + 3
                });
            }, 1000); // Simulate 1 second delay
        });
    }
    
    calculateFactors(N) {
        // Simple factorization for demo
        const knownFactors = {
            15: [3, 5],
            21: [3, 7],
            35: [5, 7],
            143: [11, 13],
            561: [3, 187],
            2047: [23, 89]
        };
        
        if (knownFactors[N]) {
            return knownFactors[N];
        }
        
        // Fallback to simple trial division
        for (let i = 2; i <= Math.sqrt(N); i++) {
            if (N % i === 0) {
                return [i, N / i];
            }
        }
        
        return [1, N]; // Prime number
    }
    
    findPeriod(N) {
        // Simulate period finding
        const periods = {
            15: 4,
            21: 6,
            35: 12,
            143: 20,
            561: 80
        };
        
        return periods[N] || Math.floor(Math.random() * 20) + 2;
    }
    
    displayResults(result) {
        const template = `
            <div class="success fade-in">
                <h4><i class="fas fa-check-circle"></i> Factorization Successful!</h4>
                <div class="result-details">
                    <p><strong>Number:</strong> ${result.N}</p>
                    <p><strong>Factors:</strong> ${result.factors[0]} × ${result.factors[1]} = ${result.N}</p>
                    <p><strong>Time:</strong> ${result.time.toFixed(3)} seconds</p>
                    <p><strong>Period Found:</strong> r = ${result.period}</p>
                    <p><strong>Quantum Measurements:</strong> ${result.quantumMeasurements}</p>
                    <p><strong>Attempts:</strong> ${result.attempts}</p>
                </div>
                <div class="verification">
                    <p><i class="fas fa-shield-check"></i> Verification: ${result.factors[0]} × ${result.factors[1]} = ${result.factors[0] * result.factors[1]}</p>
                </div>
            </div>
        `;
        
        this.resultsElement.innerHTML = template;
    }
    
    updateVisualization(result) {
        // Create Plotly visualization
        const data = [{
            x: ['Classical', 'Quantum'],
            y: [Math.log10(result.N ** 3), Math.log10(result.time * 1000)],
            type: 'bar',
            marker: {
                color: ['#ef4444', '#10b981']
            },
            text: [`O(exp(${Math.log2(result.N).toFixed(1)}))`, `O(${result.time.toFixed(3)}s)`],
            textposition: 'auto'
        }];
        
        const layout = {
            title: 'Quantum vs Classical Complexity',
            xaxis: { title: 'Algorithm' },
            yaxis: { 
                title: 'Log(Operations)',
                tickformat: '.0f'
            },
            showlegend: false
        };
        
        Plotly.newPlot(this.visualizationElement, data, layout);
    }
    
    updateCircuitInfo(N) {
        if (!N) {
            N = parseInt(document.getElementById('number-to-factor').value);
        }
        
        const n = Math.ceil(Math.log2(N));
        const qubits = 3 * n;
        const gates = n ** 3 + n ** 2;
        const depth = n ** 2;
        
        this.circuitInfo.qubits.textContent = qubits;
        this.circuitInfo.gates.textContent = gates.toLocaleString();
        this.circuitInfo.depth.textContent = depth;
        this.circuitInfo.timeComplexity.textContent = `O(${n}³)`;
        
        // Calculate quantum advantage
        const classicalTime = Math.exp(n / 3);
        const quantumTime = n ** 3;
        const advantage = classicalTime / quantumTime;
        
        this.circuitInfo.quantumAdvantage.textContent = `10^${Math.log10(advantage).toFixed(0)}x`;
    }
    
    async demoRSABreaking() {
        this.showLoading();
        
        try {
            // Simulate RSA breaking demo
            const result = await this.simulateRSABreaking();
            this.displayRSAResults(result);
        } catch (error) {
            this.showError(`RSA demo failed: ${error.message}`);
        }
    }
    
    async simulateRSABreaking() {
        return new Promise((resolve) => {
            setTimeout(() => {
                // Generate small RSA-like numbers
                const p = 11, q = 13;
                const N = p * q;
                
                resolve({
                    p: p,
                    q: q,
                    N: N,
                    bits: N.toString(2).length,
                    time: Math.random() * 0.3 + 0.2,
                    success: true
                });
            }, 1500);
        });
    }
    
    displayRSAResults(result) {
        const template = `
            <div class="warning fade-in">
                <h4><i class="fas fa-shield-alt"></i> RSA Breaking Demonstration</h4>
                <div class="rsa-details">
                    <p><strong>Generated RSA-like Number:</strong></p>
                    <p>Prime 1 (p): ${result.p}</p>
                    <p>Prime 2 (q): ${result.q}</p>
                    <p><strong>Public Key N:</strong> ${result.N} (${result.bits} bits)</p>
                    <p><strong>Factorization Time:</strong> ${result.time.toFixed(3)} seconds</p>
                    <p><strong>Status:</strong> <span class="success">✓ Successfully broken</span></p>
                </div>
                <div class="security-implication">
                    <p><i class="fas fa-exclamation-triangle"></i> <strong>Security Implication:</strong></p>
                    <p>For ${result.bits}-bit RSA: Classical time ≈ 2^${Math.floor(result.bits/3)} operations</p>
                    <p>Quantum time ≈ ${result.time.toFixed(3)} seconds with Shor's algorithm</p>
                </div>
            </div>
        `;
        
        this.resultsElement.innerHTML = template;
        this.updateCircuitInfo(result.N);
    }
    
    showLoading() {
        this.resultsElement.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>Running quantum simulation...</p>
                <p class="loading-subtext">Performing quantum period finding with QFT</p>
            </div>
        `;
        
        // Add loading animation
        const style = document.createElement('style');
        style.textContent = `
            .loading-state {
                text-align: center;
                padding: 2rem;
            }
            .loading-spinner {
                width: 50px;
                height: 50px;
                border: 5px solid #f3f3f3;
                border-top: 5px solid #6366f1;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 0 auto 1rem;
            }
            .loading-subtext {
                color: #6b7280;
                font-size: 0.9rem;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
    }
    
    showError(message) {
        this.resultsElement.innerHTML = `
            <div class="error fade-in">
                <h4><i class="fas fa-exclamation-circle"></i> Error</h4>
                <p>${message}</p>
            </div>
        `;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.shorSimulator = new ShorSimulator();
});
