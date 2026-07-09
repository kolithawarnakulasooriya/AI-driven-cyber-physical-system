import numpy as np

class KalmanFilter1D:
    """
    1D Kalman Filter with state-space representation.
    
    State vector: x = [distance]^T
    """
    
    def __init__(self, 
                dt=1.0, 
                X0=0.0,
                Q0=1e-5, 
                R0=1e-2, 
                initial_error_covariance=1.0):
        self.dt = dt
        self.q = Q0  # Process noise variance
        self.r = R0  # Measurement noise variance

        self.x = X0 # Initial state (distance)

        self.P = initial_error_covariance
        self.Q = self.q
        self.R = self.r
        
        self.estimates = []
        
    def predict(self):
        """Prediction step: x_{k|k-1} = F * x_{k-1|k-1}"""
        self.P = self.P + self.Q
        
    def update(self, z):
        """Update step with measurement z"""

        kalman_gain = self.P / (self.P + self.R)
        self.x = self.x + kalman_gain * (z - self.x)
        self.P = (1 - kalman_gain) * self.P
    
    def filter(self, measurement: float):
        """Apply Kalman filter to a single measurement"""
        self.predict()
        self.update(measurement)
        return self.x

    def filter(self, measurements: list):
        """Apply Kalman filter to a sequence of measurements"""
        self.estimates = []
        
        for measurement in measurements:
            self.predict()
            self.update(measurement)
            self.estimates.append(self.x)
            
        return self.estimates
    
    def get_state(self):
        """Return current state [position, velocity]"""
        return self.x.flatten()
    

class KalmanFilter2D:
    """
    2D Kalman Filter with state-space representation.
    
    State vector: x = [position, velocity]^T
    
    Process model:
        x_{k|k-1} = F * x_{k-1|k-1} + w_k, where w ~ N(0, Q)
    
    Measurement model:
        z_k = H * x_{k|k-1} + v_k, where v ~ N(0, R)
    
    """
    
    def __init__(self, dt=1.0, x0 = [0.0, 0.0], Q0=[1e-5,1e-5], R0=[1e-2,1e-2], e0=[1.0, 1.0]):
        self.dt = dt
        self.q = Q0  # Process noise variance
        self.r = R0  # Measurement noise variance

        # Initial state: [position, velocity]
        self.x = np.array(x0)
        
        # State transition matrix (constant velocity model)
        self.F = np.array([[1.0, dt],
                          [0.0, 1.0]])
        
        # Measurement matrix 
        # Position = 1. Position + Velocity * 0, so H = [1, 0]
        # Velocity = 0. Position + Velocity * 1, so H = [0, 1]
        self.H = np.array([[1.0, 0.0], 
                          [0.0, 1.0]])
        
        # Process noise covariance matrix
        self.Q = np.array([[self.q[0], 0.0],
                          [0.0, self.q[1]]])
        
        # Measurement noise covariance
        self.R = np.array([[self.r[0], 0.0],
                          [0.0, self.r[1]]])
        
        # Initial state error covariance
        self.P = np.eye(2) * e0
        
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
        
        for measurement in measurements:
            self.predict()
            self.update(np.array(measurement))
            self.estimates.append(self.x.flatten())
            
        return self.estimates
    
    def get_state(self):
        """Return current state [position, velocity]"""
        return self.x.flatten()