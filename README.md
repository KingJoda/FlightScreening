# FlightScreening
Launch Control Go/NoGo screening assessment for the potential impact risk of drifting debris. The screening assessment is based on an approach described in 14 CFR Part 420 Annex B1 and consists of computing impact points for a fragment with a specified, reference ballistic coefficient.


NOTE: the data field is empty - requires the following files:
• Weather profile: CSV with columns [altitude (m), density (kg/m3), u (m/s), v (m/s)]
• Trajectory: CSV with launch vehicle trajectory sample points [latitude (°), longitude (°), altitude (m)]
• DEZ: CSV with polygon vertex coordinates [latitude (°), longitude (°)]
