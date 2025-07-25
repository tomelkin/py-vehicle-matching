"""
Main module for the vehicle matcher application.
"""

import sys
import os
from db_client import DatabaseClient
from vehicle_matcher import VehicleMatcher


def process_vehicle_descriptions(filename: str) -> None:
    """
    Process a file of vehicle descriptions and show matching vehicles for each.
    
    Args:
        filename: Path to the text file containing vehicle descriptions (one per line)
    """
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return
    
    # Initialize the vehicle matcher
    try:
        db_client = DatabaseClient()
        matcher = VehicleMatcher(db_client)
    except Exception as e:
        print(f"Error initializing vehicle matcher: {e}")
        return
    
    # Read and process the file
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            descriptions = [line.strip() for line in file.readlines()]
        
        # Remove empty lines
        descriptions = [desc for desc in descriptions if desc]
        
        print(f"Vehicle Matcher - Processing {len(descriptions)} descriptions from '{filename}'")
        print("=" * 80)
        print()
        
        for i, description in enumerate(descriptions, 1):
            print(f"Input {i}: '{description}'")
            print("-" * 60)
            
            try:
                # Find matching vehicles
                vehicles = matcher.find_matching_vehicles(description)
                
                if vehicles:
                    print(f"✅ Found {len(vehicles)} matching vehicle(s):")
                    print()
                    
                    for j, vehicle in enumerate(vehicles, 1):
                        print(f"  {j}. {vehicle.make} {vehicle.model} {vehicle.badge}")
                        print(f"     Transmission: {vehicle.transmission_type}")
                        print(f"     Fuel Type: {vehicle.fuel_type}")
                        print(f"     Drive Type: {vehicle.drive_type}")
                        print(f"     Vehicle ID: {vehicle.id}")
                        if j < len(vehicles):  # Add spacing between vehicles
                            print()
                else:
                    print("❌ No matching vehicles found")
                    
            except Exception as e:
                print(f"❌ Error processing description: {e}")
            
            print()
            print("=" * 80)
            print()
    
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")


def main() -> None:
    """
    Main function to run the vehicle matcher application.
    
    Usage:
        python main.py [filename]
        
    If no filename is provided, defaults to 'inputs.txt'
    """
    # Determine input filename
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "inputs.txt"
    
    print("🚗 Vehicle Description Matcher")
    print(f"📁 Processing file: {filename}")
    print()
    
    process_vehicle_descriptions(filename)


if __name__ == "__main__":
    main() 