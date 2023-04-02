---
title: FastAPI + Selenium Webdriver
description: A FastAPI server with Selenium set up
tags:
  - fastapi
  - python
  - selenium
---

# FastAPI Example

This example starts up a [FastAPI](https://fastapi.tiangolo.com/) server with selenium already configured.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/pXu4Vv?referralCode=qL1H20)


## Link Website

https://web-production-a5a31.up.railway.app/


## ✨ Features

- FastAPI
- Python 3
- Selenium

## 💁‍♀️ How to use

- Deploy using the button 👆
- Clone locally and install packages with Pip using `pip install -r requirements.txt` or Poetry using `poetry install`
- Connect to your project using `railway link`
- Run locally using `uvicorn main:app --reload`

## 📝 Notes

- ![img](https://github.com/Ricardo-OB/coding-allstars/blob/main/imgs/img1.png)

To carry out the project, I first obtained the page with Selenium and cloned it. Then in another function I got all the translatable HTML tags (except Scripts and Styles), and then saved a file again with all the translated tags.

To load the images I had to manage the bar so that it would go through the entire page.

The translation was done with deep-translator, however, it takes a while since there are many requests to make.

## Issues:
Certain texts are not translated since they were in the middle of two labels and with the .text method they were not detected.

I couldn't translate the dropdown menus since Selenium didn't take them into account, in utils.py there is a commented code which tries to make the menus appear.