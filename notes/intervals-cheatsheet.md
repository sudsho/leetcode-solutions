# intervals cheatsheet

- digit dp: pre-compute place value contributions; saves a layer.
- monotonic stack: keep indexes, not values, when you might need positions.
- entry 99: small reminder.
- tarjan low-link refresher.
- union find rollback for offline tasks.
- meeting rooms: sort by start, overlap iff cur.start < prev.end (touching ends ok). rooms-ii needs a min-heap of end times for concurrency count.
