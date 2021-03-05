# Priya Note to the reviewer : 
# 1. Have added the token here, however, if you run my application  you will get 
# the fresh active token from the application itself. You just need to prepend it with the word Bearer
# and then add the string below
# 2. This token would have expired by the time you test, you can take the token and check for 
# permissions but during testing, use the token that's provided to you in the application.
# 3. Added the token in the config file since this is the right practice.
# 4. In addition, have set the session time for the tokens to only 2 minutes which will force you to 
# login as user and admin and generate fresh tokens for proper testing.
bearer_token = {
    'user': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFWaVo2cm5iaUw4and0VlVBejRYTSJ9.eyJpc3MiOiJodHRwczovL3ByaXNoYS5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzc5NGVjMzQ4MzgwMDZhMDQ5OWQ5IiwiYXVkIjoic3RlcHNMb2dnZXIiLCJpYXQiOjE2MTQ5ODU4NDIsImV4cCI6MTYxNDk4OTQ0MiwiYXpwIjoicVhvdDdNMVozVmxGNWUzY0hNZzdJQVh6REhETllKZEsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzdGVwcyIsImdldDpzdGVwcy1kZXRhaWwiLCJwYXRjaDpzdGVwcyIsInBvc3Q6c3RlcHMiXX0.ER9RxRj8p59VjvrAMFI2W6rGiUnwU3VJ8yARX16krc0yA0AQJ9SUi2EQkTtiDCqGpCsYwVcRyK978_YOz1liCLCoyebx3BftnCCBayXxunKXofTAQH-WMrsKdFhWUjm-7HqKkz4u12icnmzYWHu3ERLp62ehdBZcynCb1AxC8Rgb4ZKy-rUJehSGhQC6inD3-DN4OPG0JnU48Fd5vHgdiobsz6SczXWOpwup2WpcvBxgvHOkwzv58yiRGkQgzYzbqm9f1YMeXx7VR43oWgejLbtrUz8PUY4Wu0ohw55NhlttYZ_iBcjsUHeXlJ09Ro8oapXdcaXV6E9SueUwiCNWGg',
    'admin': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFWaVo2cm5iaUw4and0VlVBejRYTSJ9.eyJpc3MiOiJodHRwczovL3ByaXNoYS5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzc5ZjFhZmRmMWYwMDY5MTYwZjNjIiwiYXVkIjoic3RlcHNMb2dnZXIiLCJpYXQiOjE2MTQ5ODU2MjAsImV4cCI6MTYxNDk4OTIyMCwiYXpwIjoicVhvdDdNMVozVmxGNWUzY0hNZzdJQVh6REhETllKZEsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpzdGVwcy1hbGwiXX0.C6-6xW2-8vBb5fq_Buos1fNVtYz0JiABVhPUAk6zYTrHNQQ1LreBYY91BNiDYEtgJuUydI8c8AJF8fWHU-rrxmj9P02aZFFNc7Kq8W42ca4gf98QHYpgJYbZaayA25KDkhTFxHCBKSxlJf4proQt9ajCfCeB1kxB2W4euHH4Oq1cKuFPFcbyHOD-Dc_rfLSm11wQuvGf1_yzLKRwS8FckVjzIsZZgVHm8ewcGplgQsRTOPqCyksP0gPhsUEbmLw4AKCOatDo-wRgtkf0QsMM6vB_nBUVMg3KCx01bhIdm5mEFV6UAnEjKSfUwLB_Zdb1Dw3YTAGkXFLKcOloiSkDng'
}

configAuth0 = {
    "AUTH0_DOMAIN" : "prisha.au.auth0.com",
    "ALGORITHMS" : ["RS256"],
    "API_AUDIENCE" : "stepsLogger"
}
