while ($true) 
{
    $url = Get-Random -InputObject @("http://localhost:8080/hit", "http://localhost:8080/fail","http://localhost:8080/hello","http://localhost:8080/")
    try 
    {
        Invoke-RestMethod -Uri $url -Method Get | Out-Null
        Write-Host "Hit: $url"
    } catch 
    {
        Write-Host "Failed to hit $url"
    }
    Start-Sleep -Milliseconds (Get-Random -Minimum 1 -Maximum 10)
}





 $endpoints = @("http://localhost:8080/hit", "http://localhost:8080/fail","http://localhost:8080/hello","http://localhost:8080/")