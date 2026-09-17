#!usr/bin/env python3

import csv

MAX_CAPACITY = 10.0

def read_deliveries(filename):
    deliveries = []
    
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                delivery = {
                    'id': int(row['id']),
                    'area': row['area'],
                    'priority': int(row['priority']),
                    'weight': float(row['weight'])
                }
                deliveries.append(delivery)
            except (ValueError, KeyError, TypeError) as e:
                print(f"Skipping invalid row: {row} (reason: {e})")
    
    return deliveries

def validate_deliveries(deliveries):
    valid = []
    oversized = []

    for d in deliveries:
        if d['id'] <= 0:
            print(f"Skipping delivery {d}: invalid id")
            continue
        if d['priority'] <= 0:
            print(f"Skipping delivery {d}: invalid priority")
            continue
        if d['weight'] <= 0:
            print(f"Skipping delivery {d}: invalid weight")
            continue
        if not d['area']:
            print(f"Skipping delivery {d}: missing area")
            continue

        if d['weight'] > MAX_CAPACITY:
            print(f"Delivery {d['id']} exceeds vehicle capacity ({d['weight']}kg) - cannot be delivered")
            oversized.append(d)
            continue

        valid.append(d)

    return valid, oversized

def sort_deliveries(deliveries):
    return sorted(deliveries, key=lambda d: (d['priority'], d['area']))

def build_trip(sorted_deliveries):
    trips = []
    current_trip = []
    current_weight = 0.0


    for d in sorted_deliveries:
        fits_weight = current_weight + d['weight'] <= MAX_CAPACITY
        if fits_weight:
            current_trip.append(d)
            current_weight += d['weight']
        else:
            trips.append(current_trip)
            current_trip = [d]
            current_weight = d['weight']

    if current_trip:
        trips.append(current_trip)

    return trips

def export_trips_summary(trips, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['trip_number', 'delivery_ids', 'areas', 'num_deliveries', 'total_weight_kg', 'utilization_pct'])

        for i, trip in enumerate(trips, 1):
            delivery_ids = ','.join(str(d['id']) for d in trip)
            areas = ','.join(sorted(set(d['area'] for d in trip)))
            num_deliveries = len(trip)
            total_weight = sum(d['weight'] for d in trip)
            utilization = round((total_weight / MAX_CAPACITY) * 100, 1)

            writer.writerow([i, delivery_ids, areas, num_deliveries, total_weight, utilization])

    print(f"\nTrip summary exported to {filename}")

if __name__ == "__main__":
    deliveries = read_deliveries('../data/deliveries.csv')
    valid, oversized = validate_deliveries(deliveries)
    valid = sort_deliveries(valid)

    print("Valid deliveries:")
    for d in valid:
        print(d)
    print("Oversized deliveries:")
    for d in oversized:
        print(d)

    print("\nBuilding trips...")
    trips = build_trip(valid)
    for i, trip in enumerate(trips):
        print(f"Trip {i + 1}:")
        for d in trip:
            print(f"  Delivery ID: {d['id']}, Area: {d['area']}, Priority: {d['priority']}, Weight: {d['weight']}kg")

    export_trips_summary(trips, '../data/trips_summary.csv')