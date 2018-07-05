Super Trader
============

Now it's time to make our stock trader game - remember, greed is good!

First, import the wrapper you wrote around the Markit API. We're going to need that functionality.

Our game is going to give users a starting amount of money and let them buy and sell stocks based on the current market info we get from the Markit API. It should update their earnings whenever they login. There should be an admin. who can log-in and get an up-to-date leaderboard.

###Step 1: Database
Decide your schema. We're probably going to be adding features to this - how do we make sure it's flexible? What tables do we need?

###Step 2: Object Design
Without writing any logic, decide your functions and modules. Ask yourself the necessary questions: what properties does a user hold? What properties does a stock hold? What methods? How is the db accessed?

###Step 3: User Interface
To play our game, our users want to be able to search companies and get the exact stock ticker symbol we want. Our users also want to retreive the market data for a stock before they purchase it - we should obviously show them today's price, but we have alot more information at our disposal that will help the player make an informed decision. Start with a very simple interface that lets the users access and see this data from your API wrapper.

###Step 4: Game Logic
Now make it so users have the option to "buy" and "sell" stocks. Buying should subtract from their funds and not let them buy more than they can afford, selling should return money to their cash funds and not let them sell more than they have. Of course, users will need to buy and sell at the current rate. 

###Step 5: Views
Create a user dashboard that lets the users view their portfolio, the amount they have earned or lost, the amount of liquid cash they have available, etc. Make sure they are never looking at stale data. Think of some cool extras - maybe how their portfolio compares to the market average for the year?

###Step 6: Leaderboard
Create a superuser who can see a leaderboard that displays the top 10 users by portfolio earnings. Copy their strategy. Make millions!
