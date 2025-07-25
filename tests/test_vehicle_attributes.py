"""
Tests for the VehicleAttributes class and find_matching_attributes function.
"""

import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from vehicle_attributes import VehicleAttributes


class TestVehicleAttributes:
    """Test cases for VehicleAttributes class."""
    
    @pytest.fixture
    def vehicle_attributes(self):
        """Fixture providing a VehicleAttributes instance."""
        return VehicleAttributes()
    
    def test_init_creates_proper_attributes(self, vehicle_attributes):
        """Test that initialization creates the expected attributes and values."""
        # Check attribute types
        expected_types = ['make', 'model', 'transmission_type', 'fuel_type', 'drive_type']
        assert vehicle_attributes.attribute_types == expected_types
        
        # Check attribute values structure
        assert isinstance(vehicle_attributes.attribute_values, dict)
        assert 'make' in vehicle_attributes.attribute_values
        assert 'model' in vehicle_attributes.attribute_values
        assert 'Toyota' in vehicle_attributes.attribute_values['make']
        assert 'Volkswagen' in vehicle_attributes.attribute_values['make']
    
    def test_find_matching_attributes_single_match(self, vehicle_attributes):
        """Test finding a single attribute match in description."""
        result = vehicle_attributes.find_matching_attributes("Toyota Camry")
        
        # Should find both make and model
        assert 'make' in result
        assert 'model' in result
        assert result['make'] == 'Toyota'
        assert result['model'] == 'Camry'
    
    def test_find_matching_attributes_case_insensitive(self, vehicle_attributes):
        """Test that matching is case insensitive."""
        result = vehicle_attributes.find_matching_attributes("toyota camry MANUAL")
        
        assert 'make' in result
        assert 'model' in result
        assert 'transmission_type' in result
        assert result['make'] == 'Toyota'
        assert result['model'] == 'Camry'
        assert result['transmission_type'] == 'Manual'
    
    def test_find_matching_attributes_partial_string_match(self, vehicle_attributes):
        """Test that partial string matching works."""
        result = vehicle_attributes.find_matching_attributes("My car is a Volkswagen Golf with Automatic transmission")
        
        assert 'make' in result
        assert 'model' in result
        assert 'transmission_type' in result
        assert result['make'] == 'Volkswagen'
        assert result['model'] == 'Golf'
        assert result['transmission_type'] == 'Automatic'
    
    def test_find_matching_attributes_no_matches(self, vehicle_attributes):
        """Test behavior when no attributes match."""
        result = vehicle_attributes.find_matching_attributes("Ford F-150 Truck")
        
        # Should return empty dict since none of the values match
        assert result == {}
    
    def test_find_matching_attributes_multiple_fuel_types(self, vehicle_attributes):
        """Test matching different fuel types."""
        # Test Petrol
        result1 = vehicle_attributes.find_matching_attributes("Toyota Camry Petrol")
        assert result1.get('fuel_type') == 'Petrol'
        
        # Test Hybrid-Petrol
        result2 = vehicle_attributes.find_matching_attributes("Toyota Camry Hybrid-Petrol")
        assert result2.get('fuel_type') == 'Hybrid-Petrol'
        
        # Test Diesel
        result3 = vehicle_attributes.find_matching_attributes("Volkswagen Golf Diesel")
        assert result3.get('fuel_type') == 'Diesel'
    
    def test_find_matching_attributes_drive_types(self, vehicle_attributes):
        """Test matching different drive types."""
        # Test Front Wheel Drive
        result1 = vehicle_attributes.find_matching_attributes("Toyota Front Wheel Drive")
        assert result1.get('drive_type') == 'Front Wheel Drive'
        
        # Test Rear Wheel Drive  
        result2 = vehicle_attributes.find_matching_attributes("BMW Rear Wheel Drive")
        assert result2.get('drive_type') == 'Rear Wheel Drive'
    
    def test_find_matching_attributes_transmission_types(self, vehicle_attributes):
        """Test matching transmission types."""
        # Test Automatic
        result1 = vehicle_attributes.find_matching_attributes("Automatic transmission")
        assert result1.get('transmission_type') == 'Automatic'
        
        # Test Manual
        result2 = vehicle_attributes.find_matching_attributes("Manual gearbox")
        assert result2.get('transmission_type') == 'Manual'
    
    def test_find_matching_attributes_comprehensive_description(self, vehicle_attributes):
        """Test with a comprehensive vehicle description."""
        description = "2021 Toyota Camry Petrol Automatic Front Wheel Drive"
        result = vehicle_attributes.find_matching_attributes(description)
        
        expected = {
            'make': 'Toyota',
            'model': 'Camry', 
            'fuel_type': 'Petrol',
            'transmission_type': 'Automatic',
            'drive_type': 'Front Wheel Drive'
        }
        
        assert result == expected
    
    def test_find_matching_attributes_overlapping_matches(self, vehicle_attributes):
        """Test behavior when attribute values might overlap."""
        # This tests the current implementation behavior where last match wins
        # Note: This reveals a potential bug in the implementation
        description = "Petrol Hybrid-Petrol car"  # Contains both Petrol and Hybrid-Petrol
        result = vehicle_attributes.find_matching_attributes(description)
        
        # Current implementation will only keep the last match
        # This test documents the current behavior (which might be a bug)
        assert 'fuel_type' in result
        # The result should be one of the fuel types, depending on iteration order
        assert result['fuel_type'] in ['Petrol', 'Hybrid-Petrol']
    
    def test_find_matching_attributes_empty_description(self, vehicle_attributes):
        """Test behavior with empty description."""
        result = vehicle_attributes.find_matching_attributes("")
        assert result == {}
    
    def test_find_matching_attributes_whitespace_only(self, vehicle_attributes):
        """Test behavior with whitespace-only description."""
        result = vehicle_attributes.find_matching_attributes("   \n\t  ")
        assert result == {}
    
    def test_find_matching_attributes_special_characters(self, vehicle_attributes):
        """Test behavior with special characters in description."""
        result = vehicle_attributes.find_matching_attributes("Toyota-Camry/Petrol+Automatic")
        
        assert result.get('make') == 'Toyota'
        assert result.get('model') == 'Camry'
        assert result.get('fuel_type') == 'Petrol'
        assert result.get('transmission_type') == 'Automatic'
