from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Motorları tanımla (Döngü dışında tanımlamak daha performanslıdır)
motors = []
motor_names = ['front left propeller', 'front right propeller', 'rear left propeller', 'rear right propeller']
for name in motor_names:
    m = robot.getDevice(name)
    m.setPosition(float('inf'))
    m.setVelocity(0.0)
    motors.append(m)

# ... önceki motor tanımlamaları aynı ...

# Hover (asılı kalma) hızı genellikle 60-62 civarıdır.
# 85 çok yüksek olduğu için fırlıyor.
kalkis_hizi = 90 

while robot.step(timestep) != -1:
    # Eğer dron yerdeyse (z < 0.1), biraz daha fazla güç ver
    # Eğer havalandıysa hızı dengele
    for motor in motors:
        motor.setVelocity(kalkis_hizi)