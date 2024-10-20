# Resetting API clients

The shoppinglistapp has an API that is available to use, this is to allow you to integrate with it however you would like. If that is to create a CLI or web application, it is up to you.

However, the API relies on an API key, and sometimes API keys get lost, compromised or whatever else. Below we will go through the process of allowing a user to setup a new API key, with manual intervention from an admin.

Please do note there are steps the user should be taking before this is done but that will be covered in the API guides.

## Resetting the API client via the admin page

![Admin Page for API clients](./assets/image.png)

In the above screenshot you will see, the user/client is set to be no longer active. This means the user has reported the token as compromised. We can also imagine they want to create a new one and get access to the API again.

To do this, we will need to delete their API client. It is as simple as that, once you have done this. They can recreate a token and start consuming the APIs again.
