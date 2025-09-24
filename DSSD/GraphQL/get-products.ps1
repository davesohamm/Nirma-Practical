$headers = @{ "Content-Type" = "application/json" }
$body = @{
    query = "{ product(id:1) { id name } }"
} | ConvertTo-Json

try {
    # Invoke-RestMethod is all you need for a JSON API
    $result = Invoke-RestMethod -Uri "http://127.0.0.1:5000/graphql" -Method Post -Headers $headers -Body $body -ErrorAction Stop

    Write-Host "Response from API:"
    # Directly access and output the object
    $result | ConvertTo-Json -Depth 5 
}
catch {
    Write-Host "Error occurred:"
    Write-Host $_.Exception.Message
}
