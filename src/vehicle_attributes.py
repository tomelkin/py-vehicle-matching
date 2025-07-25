from typing import Dict

class VehicleAttributes:
    def __init__(self):
        self.attribute_types = ['make', 'model', 'transmission_type', 'fuel_type', 'drive_type']
        self.attribute_values: Dict[str, list[str]] = {
            'make': ['Toyota', 'Volkswagen'],
            'model': ['Camry', 'Golf'],
            'transmission_type': ['Automatic', 'Manual'],
            'fuel_type': ['Petrol', 'Hybrid-Petrol', 'Diesel'],
            'drive_type': ['Front Wheel Drive', 'Rear Wheel Drive']
        }
    
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