# monitoring-crypto
An example flask rest API server, for SE Fall 2022.

To build production, type `make prod`.

To create the env for a new developer, run `make dev_env`.

## Target Audience/Goal

The target audiences are primarily crypto investors based on their investment portfolio


## Requirements
* Each of the main requirements will corespond to an API endpoint.
* Main focus is on the coinmarket API

## Front-End Design
Page for user account
* Cryptocurrencies they follow
* trends/potential realtime graph of above
* Investors they follow

Search Page
* search crypto/investor option
* leading trends (e.g price change)

Investor/Cryptocurrency Page
* info on it
* price change
* market news 


## Back-End Design
Users and Systems
* Login and registration authentication
* Subscriptions for alerts (e.g. texts, emails)
* Customized alerts based on prices and activity of followed investors
* Send alerts/messages

Data Processing
* Get data from APIs chosen
* Process and analyze data for different use cases

## Database

* Store user data, e.g. account info
* Query user data, e.g. get the number of accounts
* ER Diagram: [Draw.io Design](https://drive.google.com/file/d/1_9ncNf8hwSNbuxS2CsFDgUAu4zlofcJg/view?usp=sharing) 
