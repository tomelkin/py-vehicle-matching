"""
Vehicle matching functionality using VehicleAttributes and database queries.
"""

from typing import List, Optional, Tuple, Dict
from thefuzz import fuzz
from vehicle import Vehicle
from vehicle_attributes import VehicleAttributes
from db_client import DatabaseClient
import math

class VehicleMatcher:

    def __init__(self, db_client: DatabaseClient, yaml_file: Optional[str] = None):
        self.db_client = db_client
        self.vehicle_attributes = VehicleAttributes(db_client, yaml_file)
    
    def attribute_match_confidence_score(self, matched_attributes: Dict[str, List[str]]) -> int:
        score = 0
        for _, attribute_values in matched_attributes.items():
            if len(attribute_values) == 1:
                score += 2
            else:
                score += 1
        return score

    def find_best_matching_vehicle(self, description: str) -> Tuple[Optional[Vehicle], int]:
        """
        Find the vehicle that best matches the given description. 
        
        First it checks the description for matches on all known attribute values (and aliases) 
        for: make, model, transmission type, fuel type, and drive type.

        Then it pulls back all vehicles matching these attributes from the database.

        If multiple vehicles match, it scores them using fuzzy matching algorithm.
        
        If multiple vehicles have a joint high score, it returns the one with the highest listing count.

        A confidence score out of 10 is returned, based on the number of attributes that matched.

        When multiple possible attribute values have matched the description, the confidence score will be reduced.
        
        Args:
            description (str): Natural language vehicle description 
                (e.g., 'Toyota Camry Automatic')
                
        Returns:
            Tuple[Vehicle, int]: Best matching vehicle and confidence score (0-10).
            Returns (None, 0) if no matches found.
            
        Raises:
            Exception: If database query fails.
        """
        matched_attributes = self.vehicle_attributes.find_matching_attributes(description)
        
        if not matched_attributes:
            return None, 0
        
        # Construct the SQL query
        conditions = []
        params = []
        for attribute_name, attribute_values in matched_attributes.items():
            placeholders = ", ".join(["%s"] * len(attribute_values))
            conditions.append(f"{attribute_name} IN ({placeholders})")
            params.extend(attribute_values)
        where_clause = " AND ".join(conditions)
        sql = f"""
        SELECT v.id, v.make, v.model, v.badge, v.transmission_type, v.fuel_type, v.drive_type, 
               COUNT(l.id) as listing_count
        FROM vehicle v
        LEFT JOIN listing l ON v.id = l.vehicle_id
        WHERE {where_clause}
        GROUP BY v.id
        """
        
        try:
            # Execute query
            results = self.db_client.query(sql, tuple(params))
            
            vehicles = [Vehicle.from_db_row(row) for row in results]
            

            if len(vehicles) == 0:
                return None, 0

            if (len(vehicles) == 1):
                return vehicles[0], self.attribute_match_confidence_score(matched_attributes)

            # Score each vehicle using fuzzy matching
            vehicles_with_scores = [(vehicle, fuzz.token_set_ratio(description, vehicle.get_description())) 
                            for vehicle in vehicles]
            
            top_score = max(vehicles_with_scores, key=lambda x: x[1])[1]
            vehicles_with_top_score = [v for v in vehicles_with_scores if v[1] == top_score]
            best_vehicle = max(vehicles_with_top_score, key=lambda v: v[0].listing_count)

            return best_vehicle[0], self.attribute_match_confidence_score(matched_attributes)
            
        except Exception as e:
            print(f"Database error in find_matching_vehicles: {e}")
            return [] 