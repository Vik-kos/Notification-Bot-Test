# Notification for Game Deals via Discord bot
## Introduction and Purpose

Implementation of a Discord bot using **Pycord, Playwright** and **Pytesseract**.


The Notification Bot displays the current deal from a website in a discord channel and updates if a new deal is available. Additionally a dynamic timer is displayed when the deal ends.

## Workflow
To beginn, users need to choose a channel and execute the following command: ```/start_deals```. This command triggers the bot to display the current deals. In the next step the bot captures a screenshot of the current deals and the current remaining time using **Playwright**. Additionally the screenshot of the timer is being split into three images (hours, minutes and seconds), which are then read using **Pytesseract**. Finally, all given information is being displayed via a Discord message.
## Example
![Example1](./cogs/helperfunctions/images/exampleDeal.png)