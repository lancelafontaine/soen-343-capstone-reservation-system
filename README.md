# SOEN 343 Team Project - Capstone Room Reservation System

## Quick Start Guide for Development

### Client-Side

- If you are on Windows, download [`GitBash`](https://git-for-windows.github.io/).
- Download [`Node.js`](https://nodejs.org/en/). It should come with the [`npm`](https://www.npmjs.com/) tool.
- `cd src/client/`
- `npm install -g gulp browserify`
- `npm install`
- `npm start`
- Open your browser at `http://localhost:8080`.
- Start developing. All code should automatically recompile as you change it. However, if you made a syntax error, the server will halt. You will need to `npm start` again after fixing it.


### Server-Side

- Install [`Python 2.7.9+`](https://www.python.org/downloads/release/python-2712/).
- Set `python27` and `python27/scripts` in windows environment variables
- `cd src/`
- `pip2 install -r requirements.txt`
- `cd server/`
- `python2 manage.py runserver`
