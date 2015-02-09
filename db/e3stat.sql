SELECT COUNT(*) AS `Total number of runs` from runs;

SELECT * from processing_status_codes;

SELECT processing_status_code, COUNT(*) from runs GROUP BY processing_status_code;
