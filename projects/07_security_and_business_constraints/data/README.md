# Data acquisition and observation grain

Afrobarometer and GHS-Panel

https://www.afrobarometer.org/survey-resource/nigeria-round-10-data-2024/

Keep original downloads locally in data/raw/. Obtain any provider approval yourself; never commit credentials or restricted respondent data.

The pipeline accepts a CSV containing already validated aggregate indicators, not arbitrary raw survey records. One row is one period × geography × metric × unit × statistical vintage. Required columns: period (ISO date), geography, metric, value (numeric), unit, source_url and vintage. Duplicates cause an error. Unknown values remain missing rather than zero.

Before creating input.csv from microdata, document exact variable codes, eligibility, missing response codes, survey weights, PSU and strata, and unit conversions. This mapping has NOT yet been implemented for this project. Survey opinions and business measurements are distinct populations. Do not join respondent records across surveys.
