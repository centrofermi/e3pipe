SELECT COUNT(*) AS `Total number of runs` from runs;

SELECT * from processing_status_codes;

SELECT processing_status_code, COUNT(*) from runs GROUP BY processing_status_code;

SELECT station_name, COUNT(*) from runs WHERE run_date >= '2015-02-23' GROUP BY station_name;

SELECT COUNT(*) from runs WHERE run_date >= '2015-02-23';

SELECT station_name, COUNT(*) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.8 AND num_track_events/(run_stop - run_start) > 8. AND num_track_events/(run_stop - run_start) < 80. GROUP BY station_name;

SELECT COUNT(*) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.8 AND num_track_events/(run_stop - run_start) > 8. AND num_track_events/(run_stop - run_start) < 80.;

SELECT station_name, COUNT(*) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.4 AND num_track_events/(run_stop - run_start) > 4. AND num_track_events/(run_stop - run_start) < 100. GROUP BY station_name;

SELECT COUNT(*) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.4 AND num_track_events/(run_stop - run_start) > 4. AND num_track_events/(run_stop - run_start) < 100.;


SELECT station_name, SUM(num_track_events) from runs WHERE run_date >= '2015-02-23' GROUP BY station_name;

SELECT SUM(num_track_events) from runs WHERE run_date >= '2015-02-23';

SELECT station_name, SUM(num_track_events) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.8 AND num_track_events/(run_stop - run_start) > 8. AND num_track_events/(run_stop - run_start) < 80. GROUP BY station_name;

SELECT SUM(num_track_events) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.8 AND num_track_events/(run_stop - run_start) > 8. AND num_track_events/(run_stop - run_start) < 80.;

SELECT station_name, SUM(num_track_events) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.4 AND num_track_events/(run_stop - run_start) > 4. AND num_track_events/(run_stop - run_start) < 100. GROUP BY station_name;

SELECT SUM(num_track_events) from runs WHERE run_date >= '2015-02-23' AND num_events > 1000 AND (run_stop - run_start) > 60. AND (run_stop - run_start) < 28800. AND num_track_events/num_events > 0.4 AND num_track_events/(run_stop - run_start) > 4. AND num_track_events/(run_stop - run_start) < 100.;
