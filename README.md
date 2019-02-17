# cgsbot
Cameroon GSoCers Slack Bot

## Installing cgsbot

### Dependencies

* Python 3.0 or higher



Cgsbot works only for slack integration. To install cgsbot in your slack application, perform the following sequence of test


### Deploying cgsbot on heroku.

Fork this repo and create a new app in heruko. For more details on how to create an app please refer here.
Make sure your github account is connected to your heroku dashboard. Sync your forked cgsbot repo on heruko and dont forget to export your slack api token on heroku's environment

<p align="center"><img src="https://i.imgur.com/aNiLtZ7.png"></p>


## Testing cgsbot locally.

- Clone/download cgsbot by typing the followinf command. Be sure to have [git](https://git-scm.com/downloads) installed in your PC. <br>
```git clone https://github.com/ivange94/cgsbot ```

- Install the requirements necessary in running cgsbot by typing the following command. <br>
```pip install -r requirements.txt```

- Start cgsbot inorder to listen to incoming webhooks. <br>
```python app.py```

<p align="center"><img src="https://i.imgur.com/j9u0sMg.png"></p>


- Run the sample test to simulate events, bot mentions in a real time environment by typing the following command. <br>
```python test.py```

<p align="center"><img src="https://i.imgur.com/mOoJuBj.png"></p>

- Trigger a sample ```app_mention``` event as see below

<p align="center"><img src="https://i.imgur.com/oQLwZ3i.png"></p>

- Sending response to slack bot - refer to this to change the json body in ```test.py```

<p align="center"><img src="https://i.imgur.com/MhVtuc4.png?1"></p>




