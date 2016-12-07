# SOEN 343 Team Project - Capstone Room Reservation System

## Team Members
- Rameen Rastan-Vadiveloo (27191863) / [rameenrastan](https://github.com/rameenrastan)
- Benny Zhao (27205104) / [softwarebrah](https://github.com/SoftwareBrah)
- Jason Tsalikis (25892120) / [jason10129](https://github.com/jason10129)
- Lenz Petion (26775837) / [monsieurpetion](https://github.com/monsieurpetion)
- Simeon Cvetkovic (27430515) / [cvesim](https://github.com/cvesim)
- Lance Lafontaine (26349188) / [lancelafontaine](https://github.com/lancelafontaine)
- Zhipeng Cai (21346482) / [choitwao](https://github.com/choitwao)
- Sam Alexander Moosavi (27185731) / [sammoosavi](https://github.com/sammoosavi)

## Quick Start Guide for Development

#### Developed strictly for the Google Chrome browser.

### Client-Side

- If you are on Windows, download [`GitBash`](https://git-for-windows.github.io/).
- Download [`Node.js`](https://nodejs.org/en/). It should come with the [`npm`](https://www.npmjs.com/) tool.
- `cd src/client/`
- `npm install`
- `gulp` to build the front-end and start the local server, or `npm start` start the server without build
- Open your browser at `http://localhost:8080`.
- Start developing. All code should automatically recompile as you change it. However, if you made a syntax error, the server will halt. You will need to `npm start` again after fixing it.


### Server-Side

- Install [`Python 2.7.9+`](https://www.python.org/downloads/release/python-2712/).
- Set `python27` and `python27/scripts` in windows environment variables if on Windows
- `cd src/`
- `pip2 install -r requirements.txt`
- `cd server/`
- `python2 manage.py migrate`
- `python2 manage.py shell < setupdatabase.py`
- `python2 manage.py runserver`

### User Accounts

- `testuser` / `testuser`
- `testuser2` / `testuser3`
- `testuser2` / `testuser3`


