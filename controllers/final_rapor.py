from controller import Supervisor

robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# Sahnedeki dronu DEF isminden bulalım
drone = robot.getFromDef("MAVIC_2_PRO")

print("--- LifeScan-ROS: Akıllı Tarama Sistemi Aktif ---")

while robot.step(timestep) != -1:
    drone_pos = drone.getPosition()
    root_children = robot.getRoot().getField("children")
    
    for i in range(root_children.getCount()):
        node = root_children.getMFNode(i)
        node_type = node.getTypeName()
        
        # Algılanacak nesne listesi
        targets = ["Dog", "Cat", "ScooterSimple"]
        
        if any(target in node_type for target in targets):
            obj_pos = node.getPosition()
            # Mesafe hesabı
            dist = ((drone_pos[0]-obj_pos[0])**2 + (drone_pos[2]-obj_pos[2])**2)**0.5
            
            # 3 metre yakındaysa raporla
            if dist < 3.0:
                if "Dog" in node_type or "Cat" in node_type:
                    print(f"!!! CANLI TESPİT EDİLDİ: [{node_type}] - Konum: {obj_pos[0]:.1f}, {obj_pos[2]:.1f}")
                elif "ScooterSimple" in node_type:
                    print(f"--- EKİPMAN TESPİT EDİLDİ: [Ulaşım Aracı] - Konum: {obj_pos[0]:.1f}, {obj_pos[2]:.1f}")