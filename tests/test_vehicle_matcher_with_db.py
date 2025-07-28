"""
Integration tests for the VehicleMatcher class.
"""

import pytest
from db_client import DatabaseClient
from vehicle_matcher import VehicleMatcher
from vehicle import Vehicle

@pytest.fixture(scope="module")
def db_client() -> DatabaseClient:
    return DatabaseClient()

@pytest.fixture(scope="module")
def vehicle_matcher(db_client: DatabaseClient) -> VehicleMatcher:
    return VehicleMatcher(db_client, yaml_file="vehicle_aliases.yaml")

def test_find_best_matching_vehicle_with_toyota_camry_hybrid(vehicle_matcher: VehicleMatcher):
    match, score = vehicle_matcher.find_best_matching_vehicle("Toyota Camry Hybrid")

    assert match.make == "Toyota"
    assert match.model == "Camry"
    assert match.fuel_type == "Hybrid-Petrol"
    assert score == 6

def test_find_best_matching_vehicle_with_vw_amarok_ultimate(vehicle_matcher: VehicleMatcher):
    match, score = vehicle_matcher.find_best_matching_vehicle("VW Amarok Ultimate")

    assert match.make == "Volkswagen"
    assert match.model == "Amarok"
    assert "Ultimate" in match.badge 
    assert score == 6

@pytest.mark.xfail(reason="This test checks for the right match, but our matching algorithm is not good enough yet")
def test_find_best_matching_vehicle_with_vw_golf_r_toyota_engine_swap(vehicle_matcher: VehicleMatcher):
    match, score = vehicle_matcher.find_best_matching_vehicle("VW Golf R with engine swap from Toyota 86 GT")

    assert match.make == "Volkswagen"
    assert match.model == "Golf"
    assert score == 2

def test_find_matching_vehicles_with_vw_golf_comfortline(vehicle_matcher: VehicleMatcher):
    match, score = vehicle_matcher.find_best_matching_vehicle("Volkswagen Golf 110TSI Comfortline Petrol Automatic Front Wheel Drive")

    assert match.make == "Volkswagen"
    assert match.model == "Golf"
    assert match.fuel_type == "Petrol"
    assert match.transmission_type == "Automatic"
    assert match.drive_type == "Front Wheel Drive"
    assert match.badge == "110TSI Comfortline"
    assert score == 9
