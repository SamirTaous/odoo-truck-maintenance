# Truck Maintenance Module

## Overview
The Truck Maintenance module is a comprehensive fleet management solution for managing truck vehicles, maintenance schedules, and operational tracking. This module was extracted from the Transport Management module to provide focused truck fleet management capabilities.

## Features

### Fleet Management
- **Truck Registration**: Complete truck information including specifications, dimensions, and capabilities
- **Brand Support**: Support for major truck manufacturers (Volvo, Scania, Mercedes-Benz, MAN, etc.)
- **Ownership Types**: Company owned, rented, and subcontracted vehicles
- **Driver Assignment**: Assign drivers to specific trucks

### Maintenance Management
- **Maintenance Scheduling**: Track maintenance intervals and due dates
- **Maintenance Requests**: Integration with Odoo's maintenance module
- **Maintenance Status**: Track vehicle condition (Good, Needs Attention, Critical)
- **Odometer Tracking**: Monitor vehicle usage and service intervals

### Vehicle Specifications
- **Cargo Capacity**: Weight and volume specifications
- **Dimensions**: Complete truck and cargo area measurements
- **Engine Details**: Power, fuel type, and consumption tracking
- **Special Equipment**: Crane, refrigeration, GPS tracking, etc.

### Compliance & Documentation
- **Registration Tracking**: Monitor registration expiry dates
- **Insurance Management**: Track insurance expiry dates
- **Technical Inspections**: Schedule and track mandatory inspections

## Models

### Truck Vehicle (`truck.vehicle`)
Main model for truck fleet management with comprehensive specifications and maintenance tracking.

**Key Fields:**
- Basic Information: License plate, VIN, brand, model, year
- Specifications: Payload, volume, dimensions, engine power
- Maintenance: Status, schedules, odometer readings
- Ownership: Company owned, rented, or subcontracted
- Compliance: Registration, insurance, inspection dates

## Installation
1. Install the module through Odoo Apps
2. The module depends on: `base`, `web`, `fleet`, `mail`, `maintenance`
3. Demo data includes sample trucks for testing

## Usage
1. Navigate to **Truck Maintenance** → **Fleet Management** → **Truck Fleet**
2. Create new trucks with complete specifications
3. Schedule maintenance through the maintenance requests
4. Track vehicle status and availability
5. Monitor compliance dates and renewals

## Integration
- **Transport Management**: Trucks can be assigned to transport missions
- **Maintenance Module**: Full integration with Odoo's maintenance system
- **Fleet Module**: Leverages Odoo's fleet management capabilities

## Views
- **Kanban View**: Visual fleet overview with status indicators
- **Tree View**: Tabular list with key information
- **Form View**: Detailed truck information and specifications
- **Search/Filter**: Advanced filtering by status, type, ownership, etc.