from controller import Supervisor

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())
drone = robot.getFromDef("MAVIC_2_PRO")

# --- KRİTİK DÜZELTME: DRON KALKANA KADAR TESPİTİ ERTELİYORUZ ---
print("⌛ Raporlama Merkezi: Dronun kalkması bekleniyor ...")
while robot.step(timestep) != -1:
    if robot.getTime() > 5.0:  # Dron havalandıktan sonra döngüden çık
        break

print("\n" + "="*45)
print("--- 🚀 Raporlama Merkezi: Akıllı Filtreleme Aktif ---")
print("🪁 Dron kalkışını tamamladı.")
print("🎑 Menzil Kontrolü: Dron konum merkezli 4 metre yarıçaplı alan içindeki canlılar tespit ediliyor...")
print("="*45 + "\n")

sayac = 0
raporlanan_canlilar = set()

while robot.step(timestep) != -1:
    if drone is None:
        continue
        
    sayac += 1
    if sayac % 20 != 0: # Kontrol sıklığı (her saniye bir)
        continue

    drone_pos = drone.getPosition()
    root_children = robot.getRoot().getField("children")
    
    su_an_menzildeki_canlilar = set()
    
    for i in range(root_children.getCount()):
        node = root_children.getMFNode(i)
        node_type = node.getTypeName()
        
        # Hedef nesneler listesi
        if any(target in node_type for target in ["Dog", "Cat", "ScooterSimple"]):
            obj_pos = node.getPosition()
            # Dron ile nesne arasındaki yatay mesafe
            dist = ((drone_pos[0]-obj_pos[0])**2 + (drone_pos[2]-obj_pos[2])**2)**0.5
            
            # Eğer canlı 4 metre menzile girdiyse
            if dist < 4.0:
                # KRİTİK DÜZELTME: ScooterSimple'ı da listeye ekleyebilmesi için buraya dahil ettik
                if "Dog" in node_type or "Cat" in node_type or "ScooterSimple" in node_type:
                    canli_id = f"{node_type}_{obj_pos[0]:.1f}_{obj_pos[2]:.1f}"
                    su_an_menzildeki_canlilar.add(canli_id)
                    
                    if canli_id not in raporlanan_canlilar:
                        print(f"🚨 YENİ CANLI TESPİT EDİLDİ:")
                        # İki nokta (:) hataları ve mantık blokları düzeltildi
                        if "Dog" in node_type:
                            print(f" 🐶 [Köpek] - 🚩 Konum: X={obj_pos[0]:.1f}, Z={obj_pos[2]:.1f}")
                        elif "Cat" in node_type:
                            print(f" 🐱 [Kedi] - 🚩 Konum: X={obj_pos[0]:.1f}, Z={obj_pos[2]:.1f}")
                        else:
                            print(f" 🚵‍♀️ [İnsan / Scooter] - 🚩 Konum: X={obj_pos[0]:.1f}, Z={obj_pos[2]:.1f}")

                        raporlanan_canlilar.add(canli_id)
                        
    raporlanan_canlilar = raporlanan_canlilar.intersection(su_an_menzildeki_canlilar)