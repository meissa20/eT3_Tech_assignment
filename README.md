# Delivery Route Planner

A small Python program that organizes delivery requests into vehicle trips, respecting a maximum
vehicle capacity, delivery priority, and area grouping where possible.

## Project Structure

```
.
├── data
│   ├── deliveries.csv        # sample input file
│   └── trips_summary.csv     # generated output (created after running the program)
├── src
│   └── main.py                # main program
└── tests
    └── testing.py              # test cases
```

## How to Run

1. Make sure you have Python 3 installed (no external libraries are required — only the standard library).
2. From the `src` folder, run:

```
cd src
python main.py
```

3. The program will:
   - Read deliveries from `../data/deliveries.csv`
   - Print any invalid or oversized deliveries as warnings
   - Print the sorted delivery list and the resulting trips
   - Export a trip summary to `../data/trips_summary.csv`

## Input Format

Deliveries are provided as a CSV file with the following columns:

| Column   | Type    | Description                              |
|----------|---------|-------------------------------------------|
| id       | integer | Unique delivery ID                        |
| area     | text    | Delivery area/neighborhood                |
| priority | integer | Lower number = more urgent                |
| weight   | float   | Package weight in kg                      |

Example (`data/deliveries.csv`):

```
id,area,priority,weight
1,Nasr City,2,4.5
2,Maadi,1,2.0
3,Nasr City,3,1.2
4,Zamalek,1,7.0
5,Maadi,2,3.5
```

## Running Tests

From the `tests` folder, run:

```
cd tests
python testing.py
```

This runs a set of `assert`-based checks covering the main edge cases: empty input, a single
delivery, a trip that fills exactly to capacity, a delivery that forces a new trip, an oversized
package, and priority/area sorting order.

## Extension Feature: Trip Summary Export

After building the trips, the program exports a summary CSV (`data/trips_summary.csv`) with one row
per trip, containing: trip number, the IDs of deliveries included, the areas covered, number of
deliveries, total weight, and capacity utilization percentage.

I chose this because a delivery planner is only useful if the output can be handed off — a
dispatcher or another system could use this file directly, and the utilization percentage makes it
easy to spot inefficient (under-filled) trips at a glance.

## Reasoning

### 1. Explain your solution approach in your own words.

The program works in four stages:

1. **Read** — deliveries are loaded from a CSV file into a list of dictionaries. Any row that is
   missing a field or has an invalid value (non-numeric weight, missing column, etc.) is skipped
   with a warning instead of crashing the program.
2. **Validate** — each delivery is checked for basic sanity (positive id, priority, and weight, and
   a non-empty area). Deliveries heavier than the vehicle's 10kg capacity are separated out, since
   they can never be assigned to any trip — this is not treated as bad data, but as a real delivery
   that cannot be fulfilled with the current vehicle.
3. **Sort** — valid deliveries are sorted by priority (ascending, so the most urgent deliveries come
   first), using area as a tiebreaker. This means deliveries with the same priority end up next to
   each other if they share the same area, which naturally helps with grouping in the next step.
4. **Build trips** — the sorted list is walked in order, greedily adding each delivery to the
   current trip as long as it does not exceed the 10kg capacity. As soon as adding a delivery would
   exceed the limit, the current trip is closed and a new one starts.

Because deliveries are already sorted by priority (with area as a tiebreaker) before trips are
built, urgent deliveries are always handled first, and same-area deliveries tend to end up together
naturally, without needing a separate, more complex grouping step.

### 2. What was the most difficult part of the assignment?

Balancing the two rules that can conflict: handling urgent deliveries first, and grouping
deliveries in the same area together. Strictly grouping by area first could delay urgent deliveries
in areas that get processed later; strictly following priority could break up area groupings. The
solution I settled on treats priority as the primary rule and lets area grouping happen as a
side effect of sorting (using area as a tiebreaker within the same priority), which is simple to
explain and reason about, even though it isn't a guaranteed-optimal grouping.

### 3. Are there situations where your algorithm may not produce the best possible grouping?

Yes. Two deliveries in the same area but with different priorities will not necessarily end up in
the same trip, since priority order is never broken to keep an area together. For example, if
Maadi has one delivery at priority 1 and another at priority 3, they may be split into different
trips even though grouping them would have been more efficient. The algorithm also doesn't
backtrack or reorder once a delivery has been placed into a trip, so it can't "look ahead" to find a
more efficient packing — it's a greedy approach, not an optimal one.

### 4. If the input contained 1,000,000 delivery requests, what part of your solution might become slow or memory-intensive?

- Loading a million rows into a single Python list of dictionaries would use a significant amount
  of memory, since dictionaries have more overhead per record than simpler structures (e.g. tuples,
  or a proper class with `__slots__`, or a NumPy/pandas dataframe).
- Sorting is O(n log n), which is fine even at this scale, but the `key=lambda d: (d['priority'], d['area'])`
  function is called for every comparison, and repeated dictionary lookups and string comparisons
  add overhead compared to sorting simpler, precomputed tuples.
- The trip-building loop itself is O(n) and would still be fast, but printing every delivery and
  every trip to the console (as the current version does) would be extremely slow and impractical
  at this scale — output would need to be limited to summaries, or written directly to a file
  instead of being printed.
- Reading the whole file into memory at once could also become a bottleneck; a streaming approach
  (processing rows as they're read, rather than building one big list first) would scale better.

### 5. What would you improve if you had another day to work on the solution?

- Add command-line arguments (input file path, vehicle capacity) instead of hardcoded values, to
  make the program more flexible without editing the code.
- Explore a smarter grouping algorithm (e.g. grouping by area first within each priority tier, or a
  simple bin-packing heuristic) to reduce the number of trips and improve capacity utilization,
  while still respecting priority order.
- Add more structured logging instead of `print()` statements, so warnings and skipped rows could
  be reviewed separately from normal output.
- Use a proper testing framework like `pytest` instead of manual `assert` statements, for clearer
  test output and easier expansion as more test cases are added.
- Validate that `area` and `priority` values are reasonable in a stricter sense (e.g. flag
  unreasonably large priority numbers or suspicious area names) rather than only checking for
  positivity/non-emptiness.