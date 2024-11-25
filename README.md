# Deep Learning for Stock Prediction
![ai-article-pic8](https://user-images.githubusercontent.com/62320593/95682072-4cc49280-0bb1-11eb-8433-5552044d2478.jpg)

## Background
Due to the volatility of cryptocurrency speculation, investors will often try to incorporate sentiment from social media and news articles to help guide their trading strategies. One such indicator is the Crypto Fear and Greed Index (FNG) which attempts to use a variety of data sources to produce a daily FNG value for cryptocurrency. You have been asked to help build and evaluate deep learning models using both the FNG values and simple closing prices to determine if the FNG indicator provides a better signal for cryptocurrencies than the normal closing price data.

## My Solution
To solve this problem, I have used deep learning recurrent neural networks to model bitcoin closing prices. One model uses the FNG indicators to predict the closing price while the second model uses a window of closing prices to predict the nth closing price. I split the data and used 70% for training and 30% for testing. 

From what I found, FNG indiactors does a terrible job at predicting closing price. I have experimented with different numbers windows, epochs, nodes but they made very small to no changes at all. Here is a graph showing Actual closing price vs Predicted closing price using FNG indicators:

<img width="677" alt="Screen Shot 2020-10-11 at 12 42 55 AM" src="https://user-images.githubusercontent.com/62320593/95682358-c27d2e00-0bb2-11eb-98b4-6385f45558b8.png">

##### Click [here](https://github.com/atefajmal27/Deep_Learning_for_Stock_Predictions/blob/main/%20lstm_stock_predictor_fng.ipynb) to see the code and more details.


The model with closing prices as input data however, did a much better job at predicting future closing prices. It starts off very strong and accurate but later on, it could not deal with the high volatility of bitcoin, but still the predicted closing price's trend is very similiar to actual closing price's trend. I started off with 10 day window and experimented with different numbers and it seemed that 3 days window works the best for this model. Here is a graph to show the result of Actual closing price vs Predicted closing price using previous closing prices.

<img width="677" alt="Screen Shot 2020-10-11 at 1 44 10 AM" src="https://user-images.githubusercontent.com/62320593/95682511-931af100-0bb3-11eb-9bdc-0e1b9b4eb946.png">

##### Click [here](https://github.com/atefajmal27/Deep_Learning_for_Stock_Predictions/blob/main/lstm_stock_predictor_closing.ipynb) to see the code and more details.

### Libraries and/or Modules used:
numpy <br/>
pandas <br/>
sklearn <br/>
tensorflow <br/>


