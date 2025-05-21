from PluginSimulator import PluginSimulator
from scenic.simulators.carla.simulator import CarlaSimulator
import carla
import scenic
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbosity", type=int, default=None)
    args = parser.parse_args()

    scenic.setDebuggingOptions(verbosity=args.verbosity)

    scenario = scenic.scenarioFromFile(r'C:\Users\hamze\Scenic\examples\carla\Carla_Challenge\carlaChallenge2.scenic')
    scene, _ = scenario.generate()
    simulator = PluginSimulator(
        carla_map=scene.params['carla_map'],
        map_path=scene.params['map'],
    )

    simulator.createSimulation(scene, timestep=0.1, maxSteps=1000, name='mysim')   
    


if __name__ == "__main__":
    main()
