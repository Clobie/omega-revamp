Get-ChildItem -Recurse -Include *.* | 
Get-Content | 
Measure-Object -Line