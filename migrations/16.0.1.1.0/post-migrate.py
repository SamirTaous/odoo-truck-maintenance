def migrate(cr, version):
    """
    Post-migration script to set default values for new cost fields
    """
    # Set default values for new cost fields
    cr.execute("""
        UPDATE truck_vehicle 
        SET fuel_price_per_liter = 1.50
        WHERE fuel_price_per_liter IS NULL OR fuel_price_per_liter = 0
    """)
    
    cr.execute("""
        UPDATE truck_vehicle 
        SET maintenance_cost_per_km = 0.15
        WHERE maintenance_cost_per_km IS NULL OR maintenance_cost_per_km = 0
    """)
    
    cr.execute("""
        UPDATE truck_vehicle 
        SET driver_hourly_rate = 25.00
        WHERE driver_hourly_rate IS NULL OR driver_hourly_rate = 0
    """)
    
    cr.execute("""
        UPDATE truck_vehicle 
        SET insurance_cost_per_day = 50.00
        WHERE insurance_cost_per_day IS NULL OR insurance_cost_per_day = 0
    """)
    
    cr.execute("""
        UPDATE truck_vehicle 
        SET depreciation_per_km = 0.25
        WHERE depreciation_per_km IS NULL OR depreciation_per_km = 0
    """)