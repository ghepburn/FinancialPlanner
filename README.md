# FinancialPlanner

A local command line service for analyzing personal financial data

## Set Up
1. Create virtual environment locally
2. Install dependencies from depependencies.txt file in virtual environment
3. Create a "secrets.json" file with an empty JSON object inside.
4. Add desired secrets to secrets.json. These are configurations which will not be uploaded to Github. 
5. Retrieve a "credentials.json" file from your Google Cloud Platform workspace and place it in your main directory. This authenticates you with your Google Drive API. 

## Run
1. ./env/bin/python run.py
2. Upon accessing for the first time, your web browser will ask you to log into your Google account. Please do. 
3. Once complete a token.json file will have been created in your main directory.
