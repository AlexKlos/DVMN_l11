# Space Telegram

**Space Telegram** is a Python-based project designed to download and post space-related images to a Telegram channel. The project interacts with APIs from NASA and SpaceX to fetch stunning space photos and uses a Telegram bot to share them.

## Features

- **Fetch SpaceX Launch Images**: Download photos from a specific or the latest SpaceX launch.
- **Fetch NASA APOD Images**: Download a specified number of images from NASA's Astronomy Picture of the Day (APOD).
- **Fetch NASA EPIC Images**: Download images of Earth from NASA's EPIC API.
- **Post to Telegram**: Automatically post downloaded images to a Telegram channel.

## Installation

Python3 should be already installed.
1. Clone the repository:
   ```bash
   git clone https://github.com/AlexKlos/DVMN_l11
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and fill it with the following:
   ```env
   NASA_API_KEY=your_nasa_api_key
   TELEGRAM_API_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   PAUSE_BETWEEN_POSTS=14400  # Default pause of 4 hours
   ```
If you don't have API keys or chat ID, you can use [**this inctruction**](#how-to-get-api-keys-and-chat-id) to get it.

## Usage

### Fetch Images

- **Fetch SpaceX Launch Images**:
  ```bash
  python fetch_spacex_images.py <launch_id>
  ```
  If `<launch_id>` is not provided, images from the latest launch will be downloaded.

- **Fetch NASA APOD Images**:
  ```bash
  python fetch_nasa_apod_images.py <count>
  ```
  Replace `<count>` with the number of images to download. Defaults to 1.

- **Fetch NASA EPIC Images**:
  ```bash
  python fetch_nasa_epic_images.py
  ```

### Post Images

- **Post Image to Telegram**:
  ```bash
  python post_one_image.py <filename>
  ```
  Replace `<filename>` with the name of the image to post. If not provided, a random image from the `images` folder will be posted.

- **Post all images to Telegram**:
   ```
   python post_all_image.py
   ```
   All images from the `images` folder will be posted one by one every `PAUSE_BETWEEN_POSTS` seconds. Than will be posted rendomly image from the `images` folder every `PAUSE_BETWEEN_POSTS` seconds.

## Project Structure

```
Space-Telegram/
├── images/                     # Folder containing the images
├── file_utils.py               # Module containing auxiliary functions
├── fetch_spacex_images.py      # Script to fetch SpaceX launch images
├── fetch_nasa_apod_images.py   # Script to fetch NASA APOD images
├── fetch_nasa_epic_images.py   # Script to fetch NASA EPIC images
├── post_all_images.py          # Script to post all images to Telegram
├── post_one_image.py           # Script to post one image to Telegram
├── .env                        # Environment variables
├── .gitignore                  # Ignored files
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Module Dependencies

![Module Dependencies](module_dependencies.png)
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [NASA Open APIs](https://api.nasa.gov/)
- [SpaceX API](https://github.com/r-spacex/SpaceX-API)
- [Python Telegram Bot](https://python-telegram-bot.readthedocs.io/en/stable/)

## How to get API Keys and Chat ID
- ### Obtain NASA API Key
  1. Visit the [NASA API Portal](https://api.nasa.gov/).
  2. Click on Sign Up (if you don’t have an account) or Sign In.
  3. Once logged in, click Generate API Key.
  4. Copy the generated key and paste it into the `.env` file as the value for `NASA_API_KEY`.
- ### Obtain Telegram Bot API Token
  1. Open Telegram and search for the **BotFather**.
  2. Start a chat with BotFather and send the command `/newbot`.
  3. Follow the instructions to name your bot and create a username.
  4. BotFather will provide a token for your bot. Copy this token and paste it into the `.env` file as the value for `TELEGRAM_API_TOKEN`.
- ### Get Telegram Chat ID
  1. Add your bot to the Telegram group where you want to post images.
  2. Make the bot an **admin** of the group (necessary for posting).
  3. Use the bot to send any message in the group.
  4. Open the Telegram app in your browser or use the [Telegram API](https://api.telegram.org).
  5. Retrieve the **chat ID** using the following steps:
     - Use the [Telegram Bot API](https://api.telegram.org):
     1. Send a request to:
`https://api.telegram.org/bot<TELEGRAM_API_TOKEN>/getUpdates`
(Replace <TELEGRAM_API_TOKEN> with your actual token.)
     2. Look for the `chat` field in the JSON response. The `id` in this field is your `TELEGRAM_CHAT_ID`.
  6. Copy the `chat ID` and paste it into the `.env` file as the value for `TELEGRAM_CHAT_ID`.
---
## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).

