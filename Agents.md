# Robot Configuration: 4-Link Articulated Arm

## Physical Parameters
- **Link 1 (Shoulder):** 120mm
- **Link 2 (Elbow 1):** 100mm
- **Link 3 (Elbow 2):** 80mm
- **Link 4 (Wrist/Pen holder):** 40mm
- **Total DOF:** 4 Revolute Joints + 1 End Effector Servo

## Hardware Mapping (Arduino)
- **Joint 1 (Base):** Pin 9
- **Joint 2:** Pin 10
- **Joint 3:** Pin 11
- **Joint 4:** Pin 12
- **Pen Lift (End Effector):** Pin 13
- **Serial Baud Rate:** 9600

## Operational Logic
- Use Inverse Kinematics (IK) for all rotational movements.
- Link 4 should remain perpendicular to the drawing surface (vertical).
- The Pygame interface must map a 400x400px area to the robot's physical reach.
- Always send 5 comma-separated integers followed by a newline: `j1,j2,j3,j4,pen\n`.
