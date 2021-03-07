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
    'user': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFWaVo2cm5iaUw4and0VlVBejRYTSJ9.eyJpc3MiOiJodHRwczovL3ByaXNoYS5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzc5NGVjMzQ4MzgwMDZhMDQ5OWQ5IiwiYXVkIjoic3RlcHNMb2dnZXIiLCJpYXQiOjE2MTUwNzQ1NTksImV4cCI6MTYxNTA3ODE1OSwiYXpwIjoicVhvdDdNMVozVmxGNWUzY0hNZzdJQVh6REhETllKZEsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpzdGVwcyIsImdldDpzdGVwcy1kZXRhaWwiLCJwYXRjaDpzdGVwcyIsInBvc3Q6c3RlcHMiXX0.oVFokttVUyr7xmCLB-joC8CGKqYHtVQCzIvgtMZp6eTmx5zOcRz4n9mnyRyjKDpamMLN5RYuMTMNpcWx4HQECotvb9LFJiwtm5yikUaXzKmU-Z6taoVfgH0bIyXWv5FKmPeDxuerEd0WmzCreW5sulLTgPuHx80Fkb9hqIs9UT5c_rjDLQF39Xpk88BKigw53q9dFwCLjphQ6Vrg5EpavHxE7XyFHO7y1cGHQiz79-IF9YTPpaButZwWq-VUJwa4KpXvYtybg7pN1KVV5n9-IYn5qEDPpmN4IpW9LiXdhsfSLsEUJsD8oMHnvn-4SGv1XRdGoEuEuzMsygkCy_s7pw',
    'admin': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFWaVo2cm5iaUw4and0VlVBejRYTSJ9.eyJpc3MiOiJodHRwczovL3ByaXNoYS5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNzc5ZjFhZmRmMWYwMDY5MTYwZjNjIiwiYXVkIjoic3RlcHNMb2dnZXIiLCJpYXQiOjE2MTUwNzQ3MjQsImV4cCI6MTYxNTA3ODMyNCwiYXpwIjoicVhvdDdNMVozVmxGNWUzY0hNZzdJQVh6REhETllKZEsiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpzdGVwcy1hbGwiXX0.pOLgxQTW-w23uVQWBWG2aLd3v1PqVyJk9nWY_yETXqcraAxjGM9aYCu1V6FopkJTjS03ywQRPcPfXrIcPoyx-26tThUmTAgItLkUwK2-vEUvP2wp0xgRkJT-hFs-UJmQp8cQWvGV1qv8EmovgmSkvPaPosiHAne7viE6y_d_KlQ8RElNkIU-tF5bLRh4H9iZqnAuy3_ShJG1oeazodYxNoATW_Q6kFulAzmJqSuvUVvsfAXSRFgM77uAYjbSg15sNItMeC56mUMiImmsBxX09KLrXS5Wn8nXbP_oICDvCcZdNrcUxvNbw4eDE8_WEwjkKN2F2S9zwbDkBm5gVI4uHw'
}

configAuth0 = {
    "AUTH0_DOMAIN" : "prisha.au.auth0.com",
    "ALGORITHMS" : ["RS256"],
    "API_AUDIENCE" : "stepsLogger"
}
