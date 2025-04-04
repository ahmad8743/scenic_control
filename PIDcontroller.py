import carla

class PIDcontroller():
    """ Pass in parameters for a standard PID controller"""
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kp = Kd

        self.prev_error = 0.0
        self.integral = 0.0

    def run_step(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0

        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.prev_error = error

        control = carla.VehicleControl()
        control.steer = max(-1.0, min(1.0, output))
        control.throttle = 0
        control.brake = 0

        return control