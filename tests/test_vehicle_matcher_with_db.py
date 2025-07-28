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
    return VehicleMatcher(db_client)

def test_find_matching_vehicles_with_toyota_camry(vehicle_matcher: VehicleMatcher):
    matches = vehicle_matcher.find_matching_vehicles("Toyota Camry")

    assert len(matches) == 7
    assert all(m.make == "Toyota" and m.model == "Camry" for m in matches)

def test_find_matching_vehicles_with_vw_amarok_ultimate(vehicle_matcher: VehicleMatcher):
    matches = vehicle_matcher.find_matching_vehicles("VW Amarok Ultimate")

    assert len(matches) > 0
