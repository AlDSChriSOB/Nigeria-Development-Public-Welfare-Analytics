// Set CsvPath to the absolute path of outputs/analysis.csv.
let
 CsvPath = "C:\NigeriaAnalytics\19_healthcare_and_financial_barriers\outputs\analysis.csv",
 Source = Csv.Document(File.Contents(CsvPath),[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
 Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
 Typed = Table.TransformColumnTypes(Headers,{{"period",type date},{"value",type number},{"previous_value",type number},{"absolute_change",type number},{"relative_change_pct",type number}})
in Typed
