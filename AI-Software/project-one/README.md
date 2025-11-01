# LearnHub - E-Learning Platform

A modern, responsive e-learning platform built with HTML, CSS, and JavaScript.

## Features

- 📚 6 comprehensive courses
- 🔐 User authentication (login/register)
- 📱 Fully responsive design
- ✅ Course completion tracking
- 🎨 Modern UI with smooth animations
- 💾 Local storage for data persistence

## How to Run

### Option 1: Using a Local Server (Recommended)

The platform uses JSON files which require a local server to work properly due to browser security restrictions.

**Using Python:**
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

**Using Node.js:**
```bash
# Install http-server globally
npm install -g http-server

# Run server
http-server
```

**Using PHP:**
```bash
php -S localhost:8000
```

Then open your browser and go to `http://localhost:8000`

### Option 2: Direct File Opening (Fallback)

If you can't run a local server, you can still open `index.html` directly in your browser. The platform will automatically use fallback course data instead of loading from the JSON file.

## Course Data

Courses are stored in `courses.json` and can be easily modified or extended. The platform includes:

1. 🚀 JavaScript Fundamentals
2. ⚛️ React Development  
3. 🎨 CSS Grid & Flexbox
4. 🔧 Node.js Backend
5. 🐍 Python for Data Science
6. 🎯 UI/UX Design Principles

## File Structure

```
├── index.html          # Main HTML file
├── styles.css          # All CSS styles
├── script.js           # JavaScript functionality
├── courses.json        # Course data
└── README.md          # This file
```

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Technologies Used

- HTML5
- CSS3 (Grid, Flexbox, Animations)
- Vanilla JavaScript (ES6+)
- Local Storage API
- Fetch API