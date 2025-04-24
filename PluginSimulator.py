from scenic.simulators.carla.simulator import CarlaSimulation
from scenic.domains.driving.simulators import DrivingSimulation
from scenic.domains.driving.simulators import DrivingSimulator
from scenic.simulators.carla.simulator import CarlaSimulator
from scenic.syntax.veneer import verbosePrint
import carla


class PluginSimulation(CarlaSimulation):
    def __init__(self, scene, client, tm, render, record, scenario_number, controller, **kwargs):
            super().__init__(scene, client, tm, render, record, scenario_number, **kwargs)
            
            # For now, controller must return steer, throttle, and brake values
            self.controller = controller

    def executeActions(self, allActions):
          DrivingSimulation().executeActions(allActions)
          for idx, obj in enumerate(self.agents):
            ctrl = obj._control
            if ctrl is not None:
                if idx == 0:
                    steer, throttle, brake = self.controller.run(20, 0)
                    ctrl = carla.VehicleControl(throttle=throttle, steer=steer, brake=brake)
                    obj.carlaActor.apply_control(ctrl)
                    obj._control = None
                else:
                    obj.carlaActor.apply_control(ctrl)
                    obj._control = None
                
class PluginSimulator(CarlaSimulator):
    def __init__(
        self,
        carla_map,
        map_path,
        controller,
        address="127.0.0.1",
        port=2000,
        timeout=10,
        render=True,
        record="",
        timestep=0.1,
        traffic_manager_port=None,
    ):
        DrivingSimulator.__init__(self)
        verbosePrint(f"Connecting to CARLA on port {port}")
        self.client = carla.Client(address, port)
        self.client.set_timeout(timeout)  # limits networking operations (seconds)
        if carla_map is not None:
            try:
                self.world = self.client.load_world(carla_map)
            except Exception as e:
                raise RuntimeError(f"CARLA could not load world '{carla_map}'") from e
        else:
            if str(map_path).endswith(".xodr"):
                with open(map_path) as odr_file:
                    self.world = self.client.generate_opendrive_world(odr_file.read())
            else:
                raise RuntimeError("CARLA only supports OpenDrive maps")
        self.timestep = timestep

        if traffic_manager_port is None:
            traffic_manager_port = port + 6000
        self.tm = self.client.get_trafficmanager(traffic_manager_port)
        self.tm.set_synchronous_mode(True)

        # Set to synchronous with fixed timestep
        settings = self.world.get_settings()
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = timestep  # NOTE: Should not exceed 0.1
        self.world.apply_settings(settings)
        verbosePrint("Map loaded in simulator.")

        self.render = render  # visualization mode ON/OFF
        self.record = record  # whether to use the carla recorder
        self.scenario_number = 0  # Number of the scenario executed
        self.controller = controller

    def createSimulation(self, scene, *, timestep, **kwargs):
        if timestep is not None and timestep != self.timestep:
            raise RuntimeError(
                "cannot customize timestep for individual CARLA simulations; "
                "set timestep when creating the CarlaSimulator instead"
            )

        self.scenario_number += 1
        return PluginSimulation(
            scene,
            self.client,
            self.tm,
            self.render,
            self.record,
            self.scenario_number,
            timestep=self.timestep,
            controller=self.controller,
            **kwargs,
        )
