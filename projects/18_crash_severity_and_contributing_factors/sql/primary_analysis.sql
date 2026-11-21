SELECT factor,SUM(reported_mentions) AS reported_mentions FROM factor_mentions GROUP BY factor ORDER BY reported_mentions DESC;
