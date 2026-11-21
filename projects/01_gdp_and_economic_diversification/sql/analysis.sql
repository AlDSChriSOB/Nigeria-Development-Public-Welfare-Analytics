WITH changes AS (
 SELECT *, LAG(value) OVER(PARTITION BY geography,metric,unit,vintage ORDER BY period) AS previous_value,
 LAG(period) OVER(PARTITION BY geography,metric,unit,vintage ORDER BY period) AS previous_period
 FROM observations WHERE value IS NOT NULL
)
SELECT *, value-previous_value AS absolute_change,
 CASE WHEN previous_value > 0 THEN 100.0*(value-previous_value)/previous_value END AS relative_change_pct
FROM changes ORDER BY metric,geography,period;
