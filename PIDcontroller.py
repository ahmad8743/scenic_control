class PIDcontroller:
    def __init__(self, kp, ki, kd, dt=0.01):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
    
        self.previous_error = 0
        self.integral = 0
    
    def run(self, target, current):
        error = target - current
        self.integral += error * self.dt
        derivative = (error - self.previous_error) / self.dt

        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.previous_error = error

        throttle, steer, brake = 0
        if output >= 0:
            throttle = min(output, 1.0)
            brake = 0.0
        else:
            throttle = 0.0
            brake = min(abs(output), 1.0)

        return steer, throttle, brake
