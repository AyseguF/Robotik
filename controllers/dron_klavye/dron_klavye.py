from controller import Robot, Keyboard, InertialUnit, GPS, Gyro, LED, Motor
import math

def clamp(value, low, high):
    return low if value < low else (high if value > high else value)

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Cihazlar
camera = robot.getDevice("camera")
if camera: camera.enable(timestep)

front_left_led = robot.getDevice("front left led")
front_right_led = robot.getDevice("front right led")

imu = robot.getDevice("inertial unit")
if imu: imu.enable(timestep)

gps = robot.getDevice("gps")
if gps: gps.enable(timestep)

gyro = robot.getDevice("gyro")
if gyro: gyro.enable(timestep)

keyboard = Keyboard()
keyboard.enable(timestep)

camera_roll_motor = robot.getDevice("camera roll")
camera_pitch_motor = robot.getDevice("camera pitch")

# Motorlar
front_left_motor = robot.getDevice("front left propeller")
front_right_motor = robot.getDevice("front right propeller")
rear_left_motor = robot.getDevice("rear left propeller")
rear_right_motor = robot.getDevice("rear right propeller")

MAX_MOTOR_VELOCITY = 576.0

motors = [front_left_motor, front_right_motor, rear_left_motor, rear_right_motor]
for motor in motors:
    if motor:
        motor.setPosition(float('inf'))
        motor.setVelocity(1.0)

# Motorların senkronizasyonu için 1 saniye bekleme
while robot.step(timestep) != -1:
    if robot.getTime() > 1.0:
        break

# --- EKRANA REHBERİ GERİ GETİRDİK ---
print("\n" + "="*45)
print("--- 🎉✨ GÜVENLİ PID UÇUŞ SİSTEMİ AKTİF ---")
print("🫵 Dronu kontrol etmek için 3D ekrana bir kez tıklayın.")
print("🧾 Komut Listesi:")
print("  - YUKARI OK      🔼 : İleri git")
print("  - AŞAĞI OK       🔽 : Geri git")
print("  - SOL OK         ↩️  : Kendi ekseninde sola 1-2 derece dön ")
print("  - SAĞ OK         ↪️  : Kendi ekseninde sağa 1-2 derece dön ")
print("  - SHIFT + YUKARI ⏫ : Yüksel")
print("  - SHIFT + AŞAĞI  ⏬ : Alçal")
print("  - SHIFT + SOL    ◀️  : Sola yatay kay (Strafe)")
print("  - SHIFT + SAĞ    ▶️  : Sağa yatay kay (Strafe)")
print("="*45 + "\n")

# PID Katsayıları
k_vertical_thrust = 68.5
k_vertical_offset = 0.6
k_vertical_p = 1.0   # Alçalırken ani motor kesmesini önlemek için optimize değer
k_roll_p = 40.0   
k_pitch_p = 25.0  
k_yaw_p = 1.0     # Yumuşak kilitlenme katsayısı

target_altitude = 1.2
climb_speed = 0.05
target_yaw = 0.0

# Klavye kilitleme değişkeni (Mükerrer basımı engeller)
last_key = -1

while robot.step(timestep) != -1:
    time = robot.getTime()

    # Sensörler
    roll = imu.getRollPitchYaw()[0]
    pitch = imu.getRollPitchYaw()[1]
    current_yaw = imu.getRollPitchYaw()[2] # Dronun şu an baktığı gerçek yön açısı
    
    altitude = gps.getValues()[2]
    roll_velocity = gyro.getValues()[0]
    pitch_velocity = gyro.getValues()[1]
    yaw_velocity = gyro.getValues()[2]     # Dönüş hızı
    
    # LED'ler
    led_state = int(time) % 2 == 0
    if front_left_led: front_left_led.set(led_state)
    if front_right_led: front_right_led.set(not led_state)

    # Kamera Gimbal Sınırlandırması
    if camera_roll_motor: camera_roll_motor.setPosition(clamp(-0.115 * roll_velocity, -0.4, 0.4))
    if camera_pitch_motor: camera_pitch_motor.setPosition(clamp(-0.1 * pitch_velocity, -0.4, 0.4))
    
    # Klavye Girdileri ve Rahatsızlık Değerlerinin Sıfırlanması
    roll_disturbance = 0.0
    pitch_disturbance = 0.0
    
    key = keyboard.getKey()
    is_shift = (key & Keyboard.SHIFT) != 0
    pure_key = key & ~Keyboard.SHIFT

    # --- KONSOLA YÖNLENDİRME YAZDIRMA KISMI ---
    if key > 0:
        # 1. İLERİ / GERİ / SAĞA-SOLA KAYMA (Sürekli basım isteyen dinamik hareketler)
        if not is_shift:
            if pure_key == Keyboard.UP:
                pitch_disturbance = -1.0
                print("[Komut] İleri 🔼")
            elif pure_key == Keyboard.DOWN:
                pitch_disturbance = 1.0
                print("[Komut] Geri 🔽")
        else:
            if pure_key == Keyboard.RIGHT:
                roll_disturbance = -1.0   
                print("[Komut] Sağa Yatay Kayma ▶️")
            elif pure_key == Keyboard.LEFT:
                roll_disturbance = 1.0    
                print("[Komut  Sola Yatay Kayma ◀️")
        
        # 2. DÖNÜŞ VE ALÇALMA/YÜKSELME (Sadece İLK basıldığında 1 kez tetiklenecek kısım)
        if key != last_key:
            if not is_shift:
                if pure_key == Keyboard.RIGHT:
                    target_yaw -= 0.04    
                    print(f"[Komut] Sağa Hassas Dönüş ↪️ Hedef Açı: {math.degrees(target_yaw):.1f}°")
                elif pure_key == Keyboard.LEFT:
                    target_yaw += 0.04    
                    print(f"[Komut] Sola Hassas Dönüş ↩️ Hedef Açı: {math.degrees(target_yaw):.1f}°")
            else:
                if pure_key == Keyboard.UP:
                    target_altitude += climb_speed
                    print(f"[Komut] ⏫ Yükseliyor -> Hedef Yükseklik: {target_altitude:.2f}m")
                elif pure_key == Keyboard.DOWN:
                    target_altitude -= climb_speed
                    print(f"[Komut] ⏬ Alçalıyor -> Hedef Yükseklik: {target_altitude:.2f}m")
            
            # Şu anki tuşu son basılan tuş olarak kaydet
            last_key = key
    else:
        # Hiçbir tuşa basılmıyorsa kilidi kaldır (Dizilim if key > 0 bloğunun else yapısıdır)
        last_key = -1

    # Dikey Kontrol (Alçalırken dikey girdinin alt sınırını kıstık)
    clamped_difference_altitude = clamp(target_altitude - altitude + k_vertical_offset, -0.4, 1.0)
    vertical_input = k_vertical_p * math.pow(clamped_difference_altitude, 3.0)
    
    # PID Hesaplama
    roll_input = k_roll_p * clamp(roll, -1.0, 1.0) + roll_velocity + roll_disturbance
    pitch_input = k_pitch_p * clamp(pitch, -1.0, 1.0) + pitch_velocity + pitch_disturbance
    
    # Açısal Hata Normalizasyonu (Açısal Sıçramayı Önler)
    yaw_error = target_yaw - current_yaw
    while yaw_error > math.pi: yaw_error -= 2.0 * math.pi
    while yaw_error < -math.pi: yaw_error += 2.0 * math.pi
    
    # Jiroskop sönümlemesi artırılarak ani salınımlar kilitlendi
    yaw_input = (k_yaw_p * yaw_error) + (yaw_velocity * 2.0)
    
    # MOTOR DAĞILIMINDA YAW İŞARETLERİ SENKRONİZASYONU
    front_left_input = k_vertical_thrust + vertical_input - roll_input + pitch_input + yaw_input
    front_right_input = k_vertical_thrust + vertical_input + roll_input + pitch_input - yaw_input
    rear_left_input = k_vertical_thrust + vertical_input - roll_input - pitch_input - yaw_input
    rear_right_input = k_vertical_thrust + vertical_input + roll_input - pitch_input + yaw_input
    
    # Donanımsal Limit Kırpması
    f_left_vel = clamp(front_left_input, -MAX_MOTOR_VELOCITY, MAX_MOTOR_VELOCITY)
    f_right_vel = clamp(front_right_input, -MAX_MOTOR_VELOCITY, MAX_MOTOR_VELOCITY)
    r_left_vel = clamp(rear_left_input, -MAX_MOTOR_VELOCITY, MAX_MOTOR_VELOCITY)
    r_right_vel = clamp(rear_right_input, -MAX_MOTOR_VELOCITY, MAX_MOTOR_VELOCITY)

    # Motorlara Hızları Basma (Yön uyumu yapılmış kararlı set)
    if front_left_motor: front_left_motor.setVelocity(f_left_vel)
    if front_right_motor: front_right_motor.setVelocity(-f_right_vel)
    if rear_left_motor: rear_left_motor.setVelocity(-r_left_vel)
    if rear_right_motor: rear_right_motor.setVelocity(r_right_vel)