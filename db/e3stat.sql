SELECT COUNT(*) AS `Total number of runs` from run_table;


SELECT * from processing_status_code_table;

SELECT COUNT(*) AS `Total number of runs with status code 0` from run_table WHERE processing_status_code=0;
SELECT COUNT(*) AS `Total number of runs with status code 17` from run_table WHERE processing_status_code=17;
SELECT COUNT(*) AS `Total number of runs with status code 100` from run_table WHERE processing_status_code=100;
SELECT COUNT(*) AS `Total number of runs with status code 101` from run_table WHERE processing_status_code=101;
SELECT COUNT(*) AS `Total number of runs with status code 137` from run_table WHERE processing_status_code=137;
SELECT COUNT(*) AS `Total number of runs with status code 139` from run_table WHERE processing_status_code=139;
