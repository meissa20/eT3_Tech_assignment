import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import build_trip, validate_deliveries, sort_deliveries

def test_empty_deliveries():
    deliveries = []
    valid, oversized = validate_deliveries(deliveries)
    assert valid == []
    assert oversized == []
    print("test_empty_list passed")

def test_single_delivery():
    deliveries = [{'id': 1, 'area': 'Maadi', 'priority': 1, 'weight': 5.0}]
    trips = build_trip(deliveries)
    assert len(trips) == 1
    assert trips[0][0]['id'] == 1
    print("test_single_delivery passed")

def test_exact_capacity():
    deliveries = [
        {'id': 1, 'area': 'Maadi', 'priority': 1, 'weight': 5.0},
        {'id': 2, 'area': 'Maadi', 'priority': 1, 'weight': 5.0},
    ]
    trips = build_trip(deliveries)
    assert len(trips) == 1  
    print("test_exact_capacity passed")

def test_over_capacity_splits_trip():
    deliveries = [
        {'id': 1, 'area': 'Maadi', 'priority': 1, 'weight': 5.0},
        {'id': 2, 'area': 'Maadi', 'priority': 1, 'weight': 5.1},
    ]
    trips = build_trip(deliveries)
    assert len(trips) == 2  # 5.0 + 5.1 > 10, must split
    print("test_over_capacity_splits_trip passed")

def test_oversized_package_filtered_out():
    deliveries = [{'id': 1, 'area': 'Maadi', 'priority': 1, 'weight': 15.0}]
    valid, oversized = validate_deliveries(deliveries)
    assert len(valid) == 0
    assert len(oversized) == 1
    print("test_oversized_package_filtered_out passed")

def test_sort_groups_same_priority_by_area():
    deliveries = [
        {'id': 1, 'area': 'Zamalek', 'priority': 1, 'weight': 2.0},
        {'id': 2, 'area': 'Maadi', 'priority': 1, 'weight': 2.0},
    ]
    sorted_d = sort_deliveries(deliveries)
    assert sorted_d[0]['area'] == 'Maadi'  # Maadi comes before Zamalek alphabetically
    print("test_sort_groups_same_priority_by_area passed")

if __name__ == "__main__":
    test_empty_deliveries()
    test_single_delivery()
    test_exact_capacity()
    test_over_capacity_splits_trip()
    test_oversized_package_filtered_out()
    test_sort_groups_same_priority_by_area()