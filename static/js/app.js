class SignLanguageDetector {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        
        this.isDetecting = false;
        this.detectionInterval = null;
        this.recentLetters = [];
        this.currentSentence = '';
        this.confidenceThreshold = 0.7;
        this.letterHistory = [];
        this.maxHistoryLength = 20;
        
        this.initializeElements();
        this.setupEventListeners();
        this.showLoading();
    }

    initializeElements() {
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.speakBtn = document.getElementById('speakBtn');
        this.copyBtn = document.getElementById('copyBtn');
        
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        this.currentLetter = document.getElementById('currentLetter');
        this.confidence = document.getElementById('confidence');
        this.predictedLetter = document.getElementById('predictedLetter');
        this.confidenceValue = document.getElementById('confidenceValue');
        this.sentenceText = document.getElementById('sentenceText');
        this.lettersList = document.getElementById('lettersList');
        this.detectionBox = document.getElementById('detectionBox');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.toast = document.getElementById('toast');
    }

    setupEventListeners() {
        this.startBtn.addEventListener('click', () => this.startDetection());
        this.stopBtn.addEventListener('click', () => this.stopDetection());
        this.clearBtn.addEventListener('click', () => this.clearText());
        this.speakBtn.addEventListener('click', () => this.speakText());
        this.copyBtn.addEventListener('click', () => this.copyText());
        
        // Handle visibility change to pause/resume detection
        document.addEventListener('visibilitychange', () => {
            if (document.hidden && this.isDetecting) {
                this.pauseDetection();
            } else if (!document.hidden && this.isDetecting) {
                this.resumeDetection();
            }
        });
    }

    async showLoading() {
        this.loadingOverlay.classList.add('show');
        
        try {
            // Check if model is available
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: 'test' })
            });
            
            // If we get here, the model is loaded
            setTimeout(() => {
                this.loadingOverlay.classList.remove('show');
                this.updateStatus('ready', 'Ready');
            }, 2000);
        } catch (error) {
            console.error('Model loading error:', error);
            this.loadingOverlay.classList.remove('show');
            this.updateStatus('error', 'Model Error');
            this.showToast('Error loading model. Please refresh the page.', 'error');
        }
    }

    async startDetection() {
        try {
            // Request camera access
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                }
            });
            
            this.video.srcObject = stream;
            this.video.play();
            
            // Wait for video to be ready
            this.video.addEventListener('loadedmetadata', () => {
                this.setupCanvas();
                this.startPredictionLoop();
                this.updateUI(true);
                this.updateStatus('recording', 'Detecting');
                this.showToast('Camera started successfully!', 'success');
            });
            
        } catch (error) {
            console.error('Camera access error:', error);
            this.showToast('Camera access denied. Please allow camera access.', 'error');
            this.updateStatus('error', 'Camera Error');
        }
    }

    stopDetection() {
        if (this.video.srcObject) {
            const tracks = this.video.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            this.video.srcObject = null;
        }
        
        if (this.detectionInterval) {
            clearInterval(this.detectionInterval);
            this.detectionInterval = null;
        }
        
        this.isDetecting = false;
        this.updateUI(false);
        this.updateStatus('ready', 'Ready');
        this.detectionBox.classList.remove('active');
        this.showToast('Detection stopped', 'success');
    }

    pauseDetection() {
        if (this.detectionInterval) {
            clearInterval(this.detectionInterval);
            this.detectionInterval = null;
        }
        this.updateStatus('ready', 'Paused');
    }

    resumeDetection() {
        if (this.isDetecting) {
            this.startPredictionLoop();
            this.updateStatus('recording', 'Detecting');
        }
    }

    setupCanvas() {
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
    }

    startPredictionLoop() {
        this.isDetecting = true;
        this.detectionBox.classList.add('active');
        
        this.detectionInterval = setInterval(async () => {
            if (this.video.readyState === this.video.HAVE_ENOUGH_DATA) {
                await this.captureAndPredict();
            }
        }, 500); // Predict every 500ms
    }

    async captureAndPredict() {
        try {
            // Draw current video frame to canvas
            this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            
            // Convert canvas to base64 image
            const imageData = this.canvas.toDataURL('image/jpeg', 0.8);
            
            // Send to server for prediction
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.handlePrediction(result.letter, result.confidence);
            } else {
                console.error('Prediction error:', result.error);
            }
            
        } catch (error) {
            console.error('Capture error:', error);
        }
    }

    handlePrediction(letter, confidence) {
        // Update current prediction display
        this.currentLetter.textContent = letter;
        this.confidence.textContent = `${Math.round(confidence * 100)}%`;
        this.predictedLetter.textContent = letter;
        this.confidenceValue.textContent = `${Math.round(confidence * 100)}%`;
        
        // Only process high-confidence predictions
        if (confidence >= this.confidenceThreshold && letter !== 'nothing') {
            this.processLetter(letter);
        }
        
        // Update confidence bar color
        this.updateConfidenceColor(confidence);
    }

    updateConfidenceColor(confidence) {
        const confidenceElement = this.confidence;
        if (confidence >= 0.8) {
            confidenceElement.style.color = '#48bb78'; // Green
        } else if (confidence >= 0.6) {
            confidenceElement.style.color = '#ed8936'; // Orange
        } else {
            confidenceElement.style.color = '#f56565'; // Red
        }
    }

    processLetter(letter) {
        // Add to recent letters
        this.recentLetters.push({
            letter: letter,
            timestamp: Date.now()
        });
        
        // Keep only recent letters (last 10 seconds)
        const tenSecondsAgo = Date.now() - 10000;
        this.recentLetters = this.recentLetters.filter(item => item.timestamp > tenSecondsAgo);
        
        // Update letters list display
        this.updateLettersList();
        
        // Process sentence
        this.processSentence();
    }

    updateLettersList() {
        if (this.recentLetters.length === 0) {
            this.lettersList.innerHTML = '<p class="no-letters">No letters detected yet</p>';
            return;
        }
        
        const lettersHtml = this.recentLetters
            .slice(-10) // Show last 10 letters
            .map(item => `<span class="letter-item">${item.letter}</span>`)
            .join('');
        
        this.lettersList.innerHTML = lettersHtml;
    }

    async processSentence() {
        try {
            const letters = this.recentLetters.map(item => item.letter);
            
            const response = await fetch('/process_sentence', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ letters: letters })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.currentSentence = result.sentence;
                this.sentenceText.textContent = this.currentSentence || 'Start signing to see your message appear here...';
                
                // Enable/disable speak button based on sentence content
                this.speakBtn.disabled = !this.currentSentence.trim();
            }
            
        } catch (error) {
            console.error('Sentence processing error:', error);
        }
    }

    clearText() {
        this.recentLetters = [];
        this.currentSentence = '';
        this.sentenceText.textContent = 'Start signing to see your message appear here...';
        this.lettersList.innerHTML = '<p class="no-letters">No letters detected yet</p>';
        this.speakBtn.disabled = true;
        this.showToast('Text cleared', 'success');
    }

    speakText() {
        if (!this.currentSentence.trim()) return;
        
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(this.currentSentence);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            speechSynthesis.speak(utterance);
            this.showToast('Speaking text...', 'success');
        } else {
            this.showToast('Text-to-speech not supported', 'error');
        }
    }

    async copyText() {
        if (!this.currentSentence.trim()) return;
        
        try {
            await navigator.clipboard.writeText(this.currentSentence);
            this.showToast('Text copied to clipboard!', 'success');
        } catch (error) {
            console.error('Copy error:', error);
            this.showToast('Failed to copy text', 'error');
        }
    }

    updateUI(isDetecting) {
        this.startBtn.disabled = isDetecting;
        this.stopBtn.disabled = !isDetecting;
    }

    updateStatus(type, text) {
        this.statusDot.className = `status-dot ${type}`;
        this.statusText.textContent = text;
    }

    showToast(message, type = 'success') {
        const toast = this.toast;
        const icon = toast.querySelector('.toast-icon');
        const messageEl = toast.querySelector('.toast-message');
        
        // Set icon based on type
        switch (type) {
            case 'success':
                icon.className = 'toast-icon fas fa-check-circle';
                break;
            case 'error':
                icon.className = 'toast-icon fas fa-exclamation-circle';
                break;
            case 'warning':
                icon.className = 'toast-icon fas fa-exclamation-triangle';
                break;
        }
        
        messageEl.textContent = message;
        toast.className = `toast ${type} show`;
        
        // Auto hide after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SignLanguageDetector();
});

// Handle page unload to clean up resources
window.addEventListener('beforeunload', () => {
    if (window.signLanguageDetector) {
        window.signLanguageDetector.stopDetection();
    }
});