from typing import Dict, List
from db_client import DatabaseClient

class VehicleAttributes:
    def __init__(self, db_client: DatabaseClient):
        self.db_client = db_client
        self.attribute_types = ['make', 'model', 'transmission_type', 'fuel_type', 'drive_type']
        self.attribute_values: Dict[str, List[str]] = {}
        self._load_attribute_values()
    
    def _load_attribute_values(self) -> None:
        """
        Load distinct attribute values from the database for each attribute type.
        """
        for attribute_type in self.attribute_types:
            try:
                sql = f"SELECT DISTINCT {attribute_type} FROM vehicle"
                results = self.db_client.query(sql)
                # Extract values from the result dictionaries
                self.attribute_values[attribute_type] = [row[attribute_type] for row in results]
            except Exception as e:
                print(f"Error loading {attribute_type} values: {e}")
                self.attribute_values[attribute_type] = []
    
    def find_matching_attributes(self, description: str) -> Dict[str, list[str]]:
        """
        Find the attributes that match the description.
        """
        matching_attributes = {}
        for attribute_type, attribute_values in self.attribute_values.items():
            for attribute_value in attribute_values:
                if attribute_value.lower() in description.lower():
                    matching_attributes[attribute_type] = attribute_value
        return matching_attributes