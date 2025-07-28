from typing import Dict, List, Optional
import yaml
from db_client import DatabaseClient
from vehicle_attribute import VehicleAttribute

class VehicleAttributes:
    def __init__(self, db_client: DatabaseClient, yaml_file: Optional[str] = None):
        self.db_client = db_client
        self.attribute_types = ['make', 'model', 'transmission_type', 'fuel_type', 'drive_type']
        self.attribute_values: Dict[str, List[VehicleAttribute]] = {}
        self._load_attribute_values_from_db()
        if yaml_file:
            self._load_attribute_values_from_yaml(yaml_file)
    
    def _load_attribute_values_from_db(self) -> None:
        """
        Load distinct attribute values from the database for each attribute type,
        then supplement with aliases from YAML file if provided.
        """
        # First load from database
        for attribute_type in self.attribute_types:
            try:
                sql = f"SELECT DISTINCT {attribute_type} FROM vehicle WHERE {attribute_type} IS NOT NULL"
                results = self.db_client.query(sql)
                # Create VehicleAttribute objects from database values
                self.attribute_values[attribute_type] = [
                    VehicleAttribute(name=row[attribute_type]) for row in results
                ]
            except Exception as e:
                print(f"Error loading {attribute_type} values: {e}")
                self.attribute_values[attribute_type] = []
        
    def _load_attribute_values_from_yaml(self, yaml_file) -> None:
        try:
            with open(yaml_file, 'r') as file:
                yaml_data = yaml.safe_load(file)
            
            for attribute_type, yaml_attributes in yaml_data.items():
                if attribute_type not in self.attribute_types:
                    continue
                
                existing_attrs = {attr.name: attr for attr in self.attribute_values[attribute_type]}
                
                for yaml_attr in yaml_attributes:
                    name = yaml_attr['name']
                    aliases = yaml_attr.get('aliases', [])
                    
                    if name in existing_attrs:
                        existing_attrs[name].aliases.extend(aliases)
                    else:
                        new_attr = VehicleAttribute(name=name, aliases=aliases)
                        self.attribute_values[attribute_type].append(new_attr)
        
        except Exception as e:
            print(f"Error loading YAML aliases: {e}")
    
    def find_matching_attributes(self, description: str) -> Dict[str, str]:
        """
        Find the attributes that match the description using names and aliases.
        Returns the canonical name for each matched attribute type.
        """
        matching_attributes = {}
        for attribute_type, vehicle_attributes in self.attribute_values.items():
            for vehicle_attribute in vehicle_attributes:
                if vehicle_attribute.matches(description):
                    matching_attributes[attribute_type] = vehicle_attribute.name
                    break
        return matching_attributes