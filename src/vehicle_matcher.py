"""
Vehicle matching functionality using VehicleAttributes and database queries.
"""

from typing import List
from vehicle import Vehicle
from vehicle_attributes import VehicleAttributes
from db_client import DatabaseClient


class VehicleMatcher:
    """
    A class to match vehicle descriptions to vehicle records from the database.
    """
    
    def __init__(self, db_client: DatabaseClient):
        """
        Initialize the VehicleMatcher with a database client.
        
        Args:
            db_client: DatabaseClient instance for executing database queries
        """
        self.db_client = db_client
        self.vehicle_attributes = VehicleAttributes()
    
    def find_matching_vehicles(self, description: str) -> List[Vehicle]:
        """
        Find vehicles that match the given description.
        
        Args:
            description: String describing the vehicle (e.g., 'Toyota Camry Automatic')
            
        Returns:
            List of Vehicle objects that match the description attributes
            
        Example:
            >>> matcher = VehicleMatcher(db_client)
            >>> vehicles = matcher.find_matching_vehicles('Toyota Camry Automatic')
            >>> print(f"Found {len(vehicles)} vehicles")
        """
        # Extract attributes from the description
        matched_attributes = self.vehicle_attributes.find_matching_attributes(description)
        
        # If no attributes matched, return empty list
        if not matched_attributes:
            return []
        
        # Build SQL query conditions
        conditions = []
        params = []
        
        for attribute_name, attribute_value in matched_attributes.items():
            conditions.append(f"{attribute_name} = %s")
            params.append(attribute_value)
        
        # Construct the SQL query
        where_clause = " AND ".join(conditions)
        sql = f"""
        SELECT id, make, model, badge, transmission_type, fuel_type, drive_type
        FROM vehicle 
        WHERE {where_clause}
        """
        
        try:
            # Execute the query
            results = self.db_client.query(sql, tuple(params))
            
            # Convert database rows to Vehicle objects
            vehicles = []
            for row in results:
                # Create vehicle from database row
                vehicle = Vehicle.from_db_row(row)
                vehicles.append(vehicle)
            
            return vehicles
            
        except Exception as e:
            # Log error and return empty list for graceful degradation
            print(f"Database error in find_matching_vehicles: {e}")
            return [] 