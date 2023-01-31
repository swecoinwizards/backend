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
[Figma Design](https://www.figma.com/file/C6YwbGFcm2Hhb01uTOMcQB/FinTech?node-id=0%3A1)

Login Page
* Use mongodb for logging in
* database stores username/account data
* account recovery

Sign up
* include node for buttons/activate database

Home Page - Logged In
* User personalized
* Investor/crypto movements
* Include graph based on what they follow

Home Page - Not Logged In
* Latests Trends

Investor/User Profile
* Follow github UI
* Use twitter api for tweets
* follow button
* include net worth
* show socials

User Account (logged in)
* when first logging show "Hello Name"
* Drop down settings option
* Followers/ following
* Users can follow other users
* include net worth

Search bar
* include filter for user to choose what they search for
* include auto ending?

Search Page
* search crypto/investor option
* leading trends (e.g price change)
* shows what user search for
* shows similar things with same name/searched term
* includes market cap/ popular crypto trends
* include filter

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
Database design update:
* include who users follows
* include who follows user

* Store user data, e.g. account info
* Query user data, e.g. get the number of accounts
* ER Diagram: [Draw.io Design](https://drive.google.com/file/d/1_9ncNf8hwSNbuxS2CsFDgUAu4zlofcJg/view?usp=sharing) 


# Progress and Goals

### Fall 2022 Semester
* Set up database
  + User credentials + data
* Set up coin API
  + Can request coin info
* User functions (e.g create/delete account, follow, post, etc) 
### Goals for Spring 2023 Semester
* Setting up react
  + Setting up python everywhere and getting react proj started
  + Every week add an endpoint to the react page
* Setting up authentication for user login/logout
  + Setup function (maybe w js) - 2 weeks
  + Add to react page
* Set up user notifications/alerts
  + Setup functions for each feature (e.g new posts, followers) - 4 weeks

| Tasks | Timeline |
| ---- | ---- |
| Setup React Home Page | 2/14 |
| Setup w Python Anywhere | 2/16 |
| Search bar functionality | 2/23 | 
| Login Page + login/logout functionality | 2/23 |
| User Account Page | 2/23 |
| Coin Page | 3/9 |
| Accounr Settings functionality | 3/9 |
|Email/text notification | 3/9 |
| MVP | 3/23 |
| Final modifications/additions | TBD |
