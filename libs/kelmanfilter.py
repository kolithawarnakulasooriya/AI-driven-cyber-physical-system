import numpy as np

class KalmanFilter:
    """
    1D Kalman Filter with state-space representation.
    
    State vector: x = [position, velocity]^T
    
    Process model:
        x_{k|k-1} = F * x_{k-1|k-1} + w_k, where w ~ N(0, Q)
    
    Measurement model:
        z_k = H * x_{k|k-1} + v_k, where v ~ N(0, R)
    
    Parameters:
    -----------
    dt : float
        Time step between measurements
    process_variance : float
        Process noise covariance (Q)
    measurement_variance : float
        Measurement noise covariance (R)
    initial_position : float
        Initial position estimate
    initial_velocity : float
        Initial velocity estimate
    initial_error_covariance : float
        Initial state error covariance P_0
    """
    
    def __init__(self, dt=1.0, process_variance=1e-5, measurement_variance=1e-2, 
                 initial_position=None, initial_velocity=0.0, initial_error_covariance=1.0):
        self.dt = dt
        self.q = process_variance  # Process noise variance
        self.r = measurement_variance  # Measurement noise variance
        
        # State transition matrix (constant velocity model)
        self.F = np.array([[1.0, dt],
                          [0.0, 1.0]])
        
        # Measurement matrix (we only measure position)
        self.H = np.array([[1.0, 0.0]])
        
        # Process noise covariance matrix
        self.Q = np.array([[self.q, 0.0],
                          [0.0, self.q]])
        
        # Measurement noise covariance
        self.R = np.array([[self.r]])
        
        # Initial state: [position, velocity]
        self.x = np.array([[initial_position if initial_position is not None else 0.0],
                          [initial_velocity]])
        
        # Initial state error covariance
        self.P = np.eye(2) * initial_error_covariance
        
        self.estimates = []
        self.velocities = []
        
    def predict(self):
        """Prediction step: x_{k|k-1} = F * x_{k-1|k-1}"""
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
    def update(self, z):
        """Update step with measurement z"""
        # Innovation (measurement residual)
        y = z - self.H @ self.x
        
        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman gain
        K = self.P @ self.H.T / S
        
        # State update
        self.x = self.x + K @ y
        
        # Covariance update
        self.P = (np.eye(2) - K @ self.H) @ self.P
        
    def filter(self, measurements):
        """Apply Kalman filter to a sequence of measurements"""
        self.estimates = []
        self.velocities = []
        
        for measurement in measurements:
            self.predict()
            self.update(np.array([[measurement]]))
            self.estimates.append(self.x[0, 0])
            self.velocities.append(self.x[1, 0])
            
        return self.estimates, self.velocities
    
    def get_state(self):
        """Return current state [position, velocity]"""
        return self.x.flatten()