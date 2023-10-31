# FTD-Config-SA-Icoman

## Overview

**FTD-Config-SA-Icoman** is a Python script that simplifies the process of downloading, resizing, and converting SVG icons to BMP format. This tool is designed for use with the [FreeTouchDeck (FTD)](https://github.com/DustinWatts/FreeTouchDeck) project on ESP32-based boards. With FTD-Config-SA-Icoman, you can manage your icons more efficiently.

## Features

- **Icon Fetching:** Easily download icons from a specified repository on the web.
- **Resize Icons:** Automatically resizes icons to a predefined size (e.g., 75x75) while maintaining their aspect ratio.
- **Format Conversion:** Convert downloaded SVG icons to 24-bit RGB BMP format suitable for FreeTouchDeck.

## Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/dejavu1987/ftd-config-sa-icoman.git
   ```

2. Navigate to the project directory:

   ```shell
   cd ftd-config-sa-icoman
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Modify the `icon_names` list in the `icoman.py` file with the names of the icons you want to download. Get it from https://ftd.anilmaharjan.com.np/

5. Run the script to fetch and convert the icons:

   ```shell
   python main.py
   ```

6. Icons will be downloaded, resized, and converted to BMP format. The BMP files can be found in the `icons` directory.

## Customization

You can customize the following aspects of FTD-Config-SA-Icoman:

- `ICON_REPO_RAW_BASE`: Modify the base URL of the icon repository you want to fetch icons from.
- `ICONS_DIR`: Define the directory where the icons will be stored.
- Icon size (width and height): You can customize the size by modifying the `width` and `height` variables in the code.
- File format: If you prefer a different output format, you can modify the conversion process.

## Contributing

Contributions to FTD-Config-SA-Icoman are welcome! Feel free to open issues, suggest improvements, or submit pull requests. Please follow the guidelines provided in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

FTD-Config-SA-Icoman is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For questions, issues, or feature requests, please open an issue in this repository.

---

**FTD-Config-SA-Icoman** is not affiliated with or endorsed by the [FreeTouchDeck (FTD)](https://github.com/DustinWatts/FreeTouchDeck) project. It's an independent tool created to assist FTD users in managing their icons more conveniently.
