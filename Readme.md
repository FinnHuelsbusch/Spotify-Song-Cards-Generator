# Spotify Song Cards Generator

This project generates printable PDF cards for Spotify songs or playlists. Each card includes the song's album cover, name, release date, artists, and a QR code linking to the song on Spotify. The cards are formatted into an A4-sized grid for easy printing.

## Features

- Fetches song and playlist details from Spotify.
- Generates QR codes for Spotify tracks.
- Creates printable PDF files with song details and album covers.
- Supports customizable HTML templates for front and back designs.

## Requirements

- Python 3.8 or higher
- Spotify API credentials (Client ID and Client Secret)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/FinnHuelsbusch/Spotify-Song-Cards-Generator.git
   cd Spotify-Song-Cards-Generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file for your Spotify API credentials:
   ```bash
   cp example.env .env
   ```

4. Edit the `.env` file and add your Spotify API credentials:
   ```env
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   ```

## Usage

1. Prepare an input file (`input.txt`) containing Spotify track or playlist URLs, one per line. Example:
   ```txt
   https://open.spotify.com/track/12345
   https://open.spotify.com/playlist/67890
   ```

2. Run the script:
   ```bash
   python main.py -i input.txt
   ```

3. The generated PDFs will be saved in the `output` directory.

## File Structure

- `main.py`: Main script to fetch data and generate PDFs.
- `front_template_table.html`: HTML template for the front side of the cards.
- `back_template_table.html`: HTML template for the back side of the cards.
- `requirements.txt`: Python dependencies.
- `example.env`: Template for environment variables.
- `input.txt`: Example input file with Spotify URLs.
- `output`: Directory where the generated PDFs are saved.
- `temp`: Temporary directory for intermediate files.

## Customization

- Modify `front_template_table.html` and `back_template_table.html` to customize the card design.
- Update styles or placeholders (`{SONG_NAME_0}`, `{ARTISTS_0}`, etc.) as needed.

## Example Output

- A4-sized PDF with 12 cards per page.
- Each card includes:
  - Album cover
  - Song name
  - Release date
  - Artists
  - QR code linking to the song

## Debugging

To debug the script, use the provided VS Code launch configuration in `launch.json`. It allows you to run the script with arguments directly in the integrated terminal.

## Acknowledgments

- [Spotipy](https://spotipy.readthedocs.io/) for Spotify API integration.
- [WeasyPrint](https://weasyprint.org/) for PDF generation.
- [qrcode](https://pypi.org/project/qrcode/) for QR code creation.