SELECT period,geography,metric,unit,vintage,COUNT(*) AS duplicate_count FROM observations GROUP BY period,geography,metric,unit,vintage HAVING COUNT(*)>1;
