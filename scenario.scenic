import creds
from PIDcontroller import PIDcontroller

param use2DMap = True  # Force 2D map mode
param map = localPath(creds.xodr_path)  # Set the CARLA map to use
param carla_map = 'Town05'

model scenic.simulators.carla.model  # Use the CARLA model

## CONSTANTS
EGO_MODEL = "vehicle.lincoln.mkz_2017"
EGO_SPEED = 10
EGO_BRAKING_THRESHOLD = 12

LEAD_CAR_SPEED = 10
LEADCAR_BRAKING_THRESHOLD = 10

BRAKE_ACTION = 1.0


behavior DoNothing():
    wait
## DEFINING BEHAVIORS
# EGO BEHAVIOR: Follow lane, and brake after passing a threshold distance to the leading car
behavior EgoBehavior(speed=10):
    try:
        do FollowLaneBehavior(speed)
        #do SafetyFilter()

    interrupt when withinDistanceToAnyCars(self, EGO_BRAKING_THRESHOLD):
        take SetBrakeAction(BRAKE_ACTION)
        # CBF will take control here


# LEAD CAR BEHAVIOR: Follow lane, and brake after passing a threshold distance to obstacle
behavior LeadingCarBehavior(speed=10):
    try: 
        do FollowLaneBehavior(speed)

    # interrupt when withinDistanceToAnyObjs(self, LEADCAR_BRAKING_THRESHOLD):
    #     take SetBrakeAction(BRAKE_ACTION)

## DEFINING SPATIAL RELATIONS
# make sure to put '*' to uniformly randomly select from all elements of the list, 'lanes'
lane = Uniform(*network.lanes)

obstacle = new Trash on lane.centerline
leadCar = new Car following roadDirection from obstacle for Range(-50, -30),
        with behavior LeadingCarBehavior()

ego = new Car following roadDirection from leadCar for Range(-15, -10),
        with blueprint EGO_MODEL,
        with camera Camera(fov=90, width=800, height=600)
            offset by 2 @ 0,  # 2 meters in front of the agent
        with behavior EgoBehavior()
require (distance to intersection) > 80
terminate when ego.speed < 0.1 and (distance to obstacle) < 30