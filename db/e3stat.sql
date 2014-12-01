SELECT COUNT(*) AS `Total number of runs` from run_table;

SELECT * from processing_status_code_table;

SELECT processing_status_code, COUNT(*) from run_table GROUP BY processing_status_code;
