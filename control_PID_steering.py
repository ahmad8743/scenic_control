from scenic.simulators.carla.simulator import CarlaSimulator
from scenic import scenarioFromFile
import PIDcontroller
import creds

def main():
    scenario = scenarioFromFile("scenario.scenic")
    scene, _ = scenario.generate()

    sim = CarlaSimulator(
        carla_map = scene.params['carla_map'],
        map_path = creds.xodr_path
    )
    ego_agent = scene.egoObject
    pidctrl = PIDcontroller(1, 0.1, 0.2)

    for _ in range(1000):
        control = pidctrl.run_step()
        ego_agent.apply_control(control)
        sim.step()

if __name__ == "__main__":
    main()