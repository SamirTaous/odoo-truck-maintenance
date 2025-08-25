# -*- coding: utf-8 -*-

def migrate(cr, version):
    """
    Update transport mission references after migration
    """
    if not version:
        return
    
    # Check if both tables exist
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'transport_vehicle'
        );
    """)
    transport_vehicle_exists = cr.fetchone()[0]
    
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'truck_vehicle'
        );
    """)
    truck_vehicle_exists = cr.fetchone()[0]
    
    if not transport_vehicle_exists or not truck_vehicle_exists:
        return
    
    # Update transport_mission references
    cr.execute("""
        UPDATE transport_mission 
        SET vehicle_id = truck_vehicle.id
        FROM transport_vehicle, truck_vehicle
        WHERE transport_mission.vehicle_id = transport_vehicle.id
        AND transport_vehicle.name = truck_vehicle.name;
    """)
    
    # Log the migration
    cr.execute("SELECT COUNT(*) FROM transport_mission WHERE vehicle_id IS NOT NULL;")
    updated_count = cr.fetchone()[0]
    
    if updated_count > 0:
        print(f"Updated {updated_count} transport mission vehicle references")