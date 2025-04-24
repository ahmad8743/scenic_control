from PluginSimulator import PluginSimulator
import carla
import scenic
from PIDcontroller import PIDcontroller

def main():
    pid = PIDcontroller(kp=0.5, ki=0.01, kd=0.1, dt=0.05)
    scenario = scenic.scenarioFromFile("scenario.scenic")
    scene, _ = scenario.generate()
    simulator = PluginSimulator(
        carla_map=scene.params['carla_map'],
        map_path=scene.params['map'],
        controller=pid
    )

    simulator.createSimulation(scene, timestep=0.1, maxSteps=1000, name='mysim')   


if __name__ == "__main__":
    main()
