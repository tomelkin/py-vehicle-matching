"""
Vehicle matching functionality using VehicleAttributes and database queries.
"""

from typing import List
from thefuzz import fuzz
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
        self.vehicle_attributes = VehicleAttributes(db_client)
    
    def find_matching_vehicles(self, description: str) -> List[Vehicle]:
        """
        Find vehicles that match the given description, scored and sorted by fuzzy matching.
        
        Args:
            description: String describing the vehicle (e.g., 'Toyota Camry Automatic')
            
        Returns:
            List of Vehicle objects that match the description attributes, 
            sorted by fuzzy matching score (highest to lowest)
        """
        matched_attributes = self.vehicle_attributes.find_matching_attributes(description)
        
        if not matched_attributes:
            return []
        
        # Construct the SQL query
        conditions = []
        params = []
        for attribute_name, attribute_value in matched_attributes.items():
            conditions.append(f"{attribute_name} = %s")
            params.append(attribute_value)
        where_clause = " AND ".join(conditions)
        sql = f"""
        SELECT id, make, model, badge, transmission_type, fuel_type, drive_type
        FROM vehicle 
        WHERE {where_clause}
        """
        
        try:
            # Execute query
            results = self.db_client.query(sql, tuple(params))
            
            vehicles = [Vehicle.from_db_row(row) for row in results]
            
            # Score each vehicle using fuzzy matching
            vehicle_scores = [(vehicle, fuzz.token_set_ratio(description, vehicle.get_description())) 
                            for vehicle in vehicles]
            
            # Sort by score descending and return vehicles
            vehicle_scores.sort(key=lambda x: x[1], reverse=True)
            return [vehicle for vehicle, score in vehicle_scores]
            
        except Exception as e:
            print(f"Database error in find_matching_vehicles: {e}")
            return [] 