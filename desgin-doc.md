# MOSO (Master Of Song Organization) - Application Design & Functionality Report

## Overview
MOSO is a Flask-based web application designed to manage, search, organize, and display a comprehensive library of church and worship songs. It caters to a community or choir by providing easy access to song lyrics, tracking which songs are known by the choir, analyzing song statistics, and organizing songs for specific services or events. The application deeply integrates with Microsoft OneDrive to access and parse `.docx` files containing the original song lyrics and formatting.

## Core Architecture
- **Backend Framework**: Python with Flask.
- **Authentication**: Auth0 integration (OAuth) for securing routes and managing user sessions. Access control is managed via a CSV file of allowed emails.
- **Data Storage**: Primarily file-based using JSON files (`REDergaran.json`, `wordSongsIndex.json`, `AllLyrics.json`, `song_occurrences.json`) to act as databases for song metadata, lyrics, and attributes.
- **Document Processing**: Uses `python-docx` to read `.docx` files directly from a synced OneDrive directory, extracting text, color formatting, and structure, and converting them to displayable HTML.

## Key Features & Functionality

### 1. Authentication & Authorization
- **Routes**: `/login`, `/callback`, `/logout`
- Users authenticate via Auth0. The app assigns a session and checks an `allowedEmails.csv` file to determine if the user has admin/access privileges. Unauthenticated users are treated as "Guest".

### 2. Song Retrieval & Display
- **Routes**: `/song/<book>/<songnum>`, `/docx/<WordDoc>`, `/today`
- **Functionality**: Retrieves song information from the corresponding "book" (e.g., Old, New, REDergaran). It displays lyrics by either reading cached text files or by directly accessing and parsing `.docx` files from OneDrive. It also displays "past songs" and "similar songs" by cross-referencing `song_occurrences.json` and historical data.

### 3. Search Engine
- **Routes**: `/search/<searchLyrics>`, `/attributeSearch`
- **Functionality**: Features a custom lyric search engine that uses natural language processing or regex to find songs based on lyric snippets. Furthermore, it supports attribute searching, allowing users to filter songs by attributes such as Key, Speed, Style, and Time Signature.

### 4. Organization & Indices (Tsank)
- **Routes**: `/tsank`, `/tsank_nums`, `/tsank_a_z`, `/tsank_a_z/<book>/<letter>`
- **Functionality**: Provides multiple ways to browse the song library:
  - **Thematic Index (`/tsank`)**: Organizes songs by themes.
  - **Numbered Index (`/tsank_nums`)**: Lists songs by their designated numbers within their books.
  - **Alphabetical Index (`/tsank_a_z`)**: Lists songs based on their starting letters.

### 5. Event & Service Management
- **Routes**: `/events`, `/youth`, `/newSundaySong`, `/weekdaySong`
- **Functionality**: 
  - Allows browsing and selecting songs explicitly designated for specific events (e.g., Pentecost) or groups (e.g., Youth).
  - Integrates a "Song Curator" that suggests song lineups for Sundays or weekdays based on defined constraints (e.g., first two songs, worship songs, exact order).

### 6. Song Metadata Editing
- **Route**: `/editsongs`
- **Functionality**: Provides a user interface to edit a song's attributes (Key, Speed, Style, Song Type, Time Signature, Comments). The modifications are written back directly to the corresponding JSON database files.

### 7. Repertoire Tracking (Known/Past Songs)
- **Routes**: `/known_songs`, `/past_songs`
- **Functionality**: Tracks the history of when songs were played. Allows the choir/administrators to mark songs as "known," "skipped," or played on specific types of days (Holiday, Sunday, Weekday).

### 8. Song Analysis
- **Route**: `/song_analysis`
- **Functionality**: Aggregates data from the JSON files to provide analytical insights into the repertoire. It displays distributions of song keys, tempos (slow, medium, fast), styles, and types, along with the most common combinations of these attributes.

### 9. Playlists
- **Routes**: `/playlist`, `/playlist/manage`, `/playlist/manage/add`
- **Functionality**: Basic endpoints and templates designated for creating and managing custom playlists for services.

## Templates Directory Structure
The `templates/` directory contains HTML files mapped to the various routes:
- **Core UI**: `base.html`, `index.html`
- **Auth**: `login.html`, `callback.html`, `guest.html`, `noAccess.html`
- **Song Display**: `song.html`, `display_docx.html`, `song_info.html`, `songLyr.html`
- **Indices & Search**: `search.html`, `tema.html`, `temas.html`, `temma_numbered.html`, `tsank_A_Z.html`, `tsank_letter.html`
- **Management & Editing**: `edit_songs.html`, `known_songs.html`, `check_past_songs.html`
- **Analysis & Curating**: `song_analysis.html`, `newSundaySongs.html`, `newWeekdaySongs.html`, `event.html`, `youth.html`
- **Playlists**: `playlist.html`, `playlist_manage.html`, `playlist_add.html`

## Conclusion
The application acts as a comprehensive digital hymnal and choir management system. It bridges traditional document storage (OneDrive Word documents) with a modern, searchable, and analytical web interface, streamlining the process of planning services and maintaining a musical repertoire.