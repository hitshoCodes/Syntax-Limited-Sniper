# 🚀 Automatic Syntax Limited Sniper

**Automatic Syntax Limited Sniper** is a Python script designed for sniping limited items on [Syntax.eco](https://www.syntax.eco/). This tool streamlines the sniping process, making it accessible for both beginners and experienced users. It comprises two main components: an autosearch module and a buyer module. The autosearch module continuously monitors the marketplace for newly listed limited items, while the buyer module efficiently purchases the desired items.

## 🌟 Key Features

- **Autosearch Module**: Continuously scans the marketplace for newly listed limited items and provides real-time updates.

- **Buyer Module**: Automatically purchases limited items when they become available, based on predefined criteria.

- **Customization**: Configure the tool using a simple `settings.json` file to target specific limited items and set purchasing rules.

## ❗️ Important Note

Please be aware that this tool is specifically designed to work with the website [Syntax.eco](https://www.syntax.eco/) and requires Chromium to function.

## 🚀 Getting Started

To get started with Automatic Syntax Limited Sniper, follow these simple steps:

1. Install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

2. Install Chromium on your system.

3. Open the `settings.json` file using a text editor.

4. Customize the settings based on your preferences:

```json
{
  "BUY_COOKIE": "COOKIE HERE",
  "AUTOSEARCH_COOKIE": "COOKIE HERE",
  "HIDE_ACCOUNT_NAME": false,
  "DISCORD_WEBHOOK": "WEBHOOK HERE",
  "CHECK_TIME": 1
}
```

5. Save your changes in the `settings.json` file.

### Usage

1. Run the program:

```bash
python main.py
```

That's it! You don't need to touch the `main.py` file unless you want to make improvements to the program. The simplified setup allows beginners to start sniping limited items with ease.

## ✨ Disclaimer

This tool is provided for educational and research purposes only. It is essential to use it responsibly and adhere to the terms of service of the online marketplace. Unauthorized or unethical usage of this tool is strictly prohibited, and the authors assume no responsibility for any misuse.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Elevate your limited item sniping game with Automatic Syntax Limited Sniper! Happy sniping! 🎯🛍️
