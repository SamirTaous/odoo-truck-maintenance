# -*- coding: utf-8 -*-

def migrate(cr, version):
    """
    Migrate transport.vehicle records to truck.vehicle
    """
    if not version:
        return
    
    # Check if transport.vehicle table exists
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'transport_vehicle'
        );
    """)
    
    if not cr.fetchone()[0]:
        return
    
    # Create truck_vehicle table if it doesn't exist
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'truck_vehicle'
        );
    """)
    
    if not cr.fetchone()[0]:
        # The table will be created by the ORM, so we'll handle this in post-migrate
        return
    
    # Copy data from transport_vehicle to truck_vehicle
    cr.execute("""
        INSERT INTO truck_vehicle (
            name, active, license_plate, vin_number, year, brand, model_name,
            ownership_type, rental_start_date, rental_end_date, rental_cost_per_day,
            subcontractor_id, driver_id, truck_type, max_payload, cargo_volume,
            cargo_length, cargo_width, cargo_height, overall_length, overall_width,
            overall_height, gross_vehicle_weight, engine_power, fuel_type,
            fuel_capacity, fuel_consumption, has_crane, has_tailgate,
            has_refrigeration, has_gps, special_equipment, registration_expiry,
            insurance_expiry, inspection_due, currency_id, purchase_price,
            current_value, company_id, create_uid, create_date, write_uid, write_date
        )
        SELECT 
            name, active, license_plate, vin_number, year, brand, model_name,
            ownership_type, rental_start_date, rental_end_date, rental_cost_per_day,
            subcontractor_id, driver_id, truck_type, max_payload, cargo_volume,
            cargo_length, cargo_width, cargo_height, overall_length, overall_width,
            overall_height, gross_vehicle_weight, engine_power, fuel_type,
            fuel_capacity, fuel_consumption, has_crane, has_tailgate,
            has_refrigeration, has_gps, special_equipment, registration_expiry,
            insurance_expiry, inspection_due, currency_id, purchase_price,
            current_value, company_id, create_uid, create_date, write_uid, write_date
        FROM transport_vehicle
        WHERE NOT EXISTS (
            SELECT 1 FROM truck_vehicle WHERE truck_vehicle.name = transport_vehicle.name
        );
    """)