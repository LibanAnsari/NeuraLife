<<<<<<< HEAD
# 🛡️ NeuraLife Admin Portal

A modern, responsive admin dashboard for managing the NeuraLife mental health platform.

## 🌟 Features

### 🎨 Design & UI
- **Modern Interface**: Clean, professional design matching the main user portal
- **Dark Mode Toggle**: Switch between light and dark themes with persistent storage
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Smooth Animations**: Fade-in effects, hover transitions, and loading states
- **Color-coded Stats**: Visual indicators for different data types

### 📊 Dashboard Overview
- **Real-time Statistics**:
  - Total registered users
  - Premium members count
  - Active therapists
  - Total therapy sessions
- **Visual Cards**: Beautiful gradient cards with icons and stats
- **Auto-refresh**: Dashboard updates automatically

### 👥 User Management
- View all registered users
- Search users by username or email
- See user details:
  - Username and email
  - Premium status (Free/Premium)
  - NeuraCoins balance
  - Registration date
- **Quick Actions**:
  - Grant premium status
  - Revoke premium status
- Profile avatars with user initials

### 🩺 Therapist Management
- View all registered therapists
- Therapist information:
  - Name and email
  - Specialization
  - Avatar/emoji
  - Total sessions conducted
- Track therapist activity

### 📅 Session Management
- View all therapy session bookings
- Session details:
  - User and therapist names
  - Session type (In Person, Video Call, Chat)
  - Date and time
  - Status (pending, accepted, rejected, completed)
- Color-coded status indicators:
  - 🟡 Yellow: Pending
  - 🟢 Green: Accepted
  - 🔴 Red: Rejected
  - 🔵 Blue: Completed

### 📊 Quiz Results Analytics
- View all assessment completions
- Assessment data:
  - User who took the quiz
  - Assessment type (PHQ-9, GAD-7, PSS-10)
  - Score and result
  - Completion date
- Track mental health trends

### 🔐 Security
- Secure admin login
- Hardcoded credentials (admin1 / 123456)
- Session persistence
- Logout functionality

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+ installed
- NeuraLife backend running on `http://localhost:8000`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation & Setup

1. **Navigate to admin portal directory**:
   ```bash
   cd admin-portal
   ```

2. **Start the admin server** (Windows):
   ```bash
   start_admin.bat
   ```

   Or manually:
   ```bash
   python server.py
   ```

3. **Open in browser**:
   ```
   http://localhost:9000
   ```

4. **Login**:
   - Username: `admin1`
   - Password: `123456`

---

## 🎯 Usage Guide

### Login
1. Open `http://localhost:9000` in your browser
2. Enter credentials:
   - Username: **admin1**
   - Password: **123456**
3. Click "Sign In"

### Dashboard Navigation
- **Stats Cards**: View key metrics at the top
- **Tabs**: Click tabs to switch between sections:
  - 👥 Users
  - 🩺 Therapists
  - 📅 Sessions
  - 📊 Quiz Results

### User Management
1. Click "Users" tab
2. Use search bar to filter users
3. View user details in the table
4. Click "Grant Premium" or "Revoke Premium" to change status

### Dark Mode
- Click the 🌙 moon icon (light mode) or ☀️ sun icon (dark mode)
- Theme preference is saved automatically
- Applies to entire admin interface

### Logout
- Click "Logout" button in top-right corner
- Returns to login screen
- Clears admin session

---

## 🎨 Theme & Design

### Color Palette

#### Light Mode
- **Background**: Gradient blue/purple/pink (`#dbeafe → #e9d5ff → #fce7f3`)
- **Cards**: White (`#ffffff`)
- **Text**: Gray shades (`#1f2937`, `#6b7280`)
- **Accent**: Purple/Indigo gradient (`#667eea → #764ba2`)

#### Dark Mode
- **Background**: Gradient dark blue/purple (`#1e293b → #312e81 → #4c1d95`)
- **Cards**: Dark gray (`#1f2937`)
- **Text**: Light gray/white (`#f3f4f6`, `#ffffff`)
- **Accent**: Purple/Indigo gradient (same)

### Typography
- **Font**: Inter (Google Fonts)
- **Headings**: Bold, 24-32px
- **Body**: Regular, 14-16px
- **Labels**: Semibold, 12-14px

### Components
- **Buttons**: Rounded, gradient backgrounds, hover effects
- **Cards**: Rounded corners, shadows, hover animations
- **Tables**: Alternating row hover, responsive columns
- **Badges**: Rounded pills with color coding

---

## 🔌 API Endpoints

The admin portal connects to these backend endpoints:

### Statistics
- `GET /api/admin/users` - Get all users
- `GET /api/admin/therapists` - Get all therapists
- `GET /api/admin/sessions` - Get all sessions
- `GET /api/admin/quiz-results` - Get all quiz results
- `GET /api/admin/stats` - Get overall statistics

### Actions
- `PUT /api/admin/users/{username}/premium` - Toggle premium status

---

## 📱 Responsive Design

### Desktop (1024px+)
- 4-column stat cards
- Full-width tables
- Expanded navigation

### Tablet (768px - 1023px)
- 2-column stat cards
- Scrollable tables
- Compact navigation

### Mobile (< 768px)
- Single-column layout
- Stacked stat cards
- Mobile-optimized tables
- Hamburger menu (future)

---

## 🛠️ Technical Stack

### Frontend
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first styling via CDN
- **Vanilla JavaScript**: No frameworks, pure JS
- **CSS Grid & Flexbox**: Responsive layouts

### Backend Integration
- **Fetch API**: Async data loading
- **REST API**: JSON communication
- **CORS**: Cross-origin resource sharing

### Server
- **Python HTTP Server**: Built-in `http.server` module
- **Port**: 9000
- **Static files**: HTML, JS, CSS

---

## 🎭 Features Showcase

### Stats Cards
```
┌─────────────────────┐  ┌─────────────────────┐
│  👥                 │  │  ⭐                 │
│  Users              │  │  Premium            │
│                     │  │                     │
│  125                │  │  45                 │
│  Total Registered   │  │  Premium Members    │
└─────────────────────┘  └─────────────────────┘
```

### User Table
```
Username    Email           Premium    Coins    Actions
---------------------------------------------------------
test1       test1@...      ⭐ Premium   500    [Revoke]
newuser     new@...        Free          0     [Grant]
liban       liban@...      Free        1200    [Grant]
```

### Session Status Colors
- 🟡 **Pending**: Yellow badge
- 🟢 **Accepted**: Green badge
- 🔴 **Rejected**: Red badge
- 🔵 **Completed**: Blue badge

---

## 🚨 Troubleshooting

### Admin portal won't start
**Issue**: Server won't start on port 9000
**Solution**: 
```bash
# Check if port is in use
netstat -ano | findstr :9000

# Kill process if needed
taskkill /PID <PID> /F

# Or use different port in server.py
```

### Can't login
**Issue**: Credentials not working
**Solution**: 
- Verify username: `admin1` (all lowercase)
- Verify password: `123456`
- Clear browser cache and cookies
- Try incognito/private mode

### Data not loading
**Issue**: Tables are empty or show no data
**Solution**:
1. Verify backend is running on `http://localhost:8000`
2. Check browser console for errors (F12)
3. Verify CORS is enabled in backend
4. Test API endpoints directly:
   ```
   http://localhost:8000/api/admin/users
   ```

### Dark mode not persisting
**Issue**: Theme resets on page reload
**Solution**:
- Check browser allows localStorage
- Disable "Clear cookies on exit"
- Try different browser

---

## 🔒 Security Notes

### Current Implementation
- **Hardcoded credentials**: Username and password are in JavaScript
- **No encryption**: Login data sent in plain text
- **No session tokens**: Uses localStorage flag
- **No API authentication**: Admin endpoints are unprotected

### Production Recommendations
⚠️ **DO NOT use this in production without:**
1. **Real authentication**: JWT tokens, OAuth, or similar
2. **Encrypted connections**: HTTPS/SSL certificates
3. **API security**: Admin API key or token validation
4. **Rate limiting**: Prevent brute force attacks
5. **Audit logging**: Track admin actions
6. **Role-based access**: Different admin permission levels

---

## 📂 File Structure

```
admin-portal/
├── index.html          # Main HTML file
├── app.js             # JavaScript logic
├── server.py          # Python HTTP server
├── start_admin.bat    # Windows startup script
└── README.md          # This file
```

---

## 🎯 Future Enhancements

### Planned Features
- [ ] Export data to CSV/Excel
- [ ] Advanced filtering and sorting
- [ ] Data visualization charts (graphs, pie charts)
- [ ] Bulk operations (batch premium grants)
- [ ] Email notification system
- [ ] User activity timeline
- [ ] Therapist performance metrics
- [ ] Revenue analytics
- [ ] System health monitoring
- [ ] Real-time updates (WebSocket)

### UI Improvements
- [ ] Mobile hamburger menu
- [ ] Pagination for large tables
- [ ] Column sorting
- [ ] Advanced search filters
- [ ] Data export buttons
- [ ] Confirmation modals
- [ ] Toast notifications
- [ ] Loading skeletons

---

## 📞 Support

For issues or questions:
1. Check browser console (F12) for errors
2. Verify backend is running
3. Review this README
4. Check CORS settings in backend

---

## 📄 License

Part of the NeuraLife platform. All rights reserved.

---

## 🎉 Credits

**Design**: Modern admin dashboard inspired by contemporary SaaS platforms
**Theme**: Matches NeuraLife user portal branding
**Icons**: Emoji-based for universal compatibility

---

**Happy Managing! 🚀**
=======
# 🛡️ NeuraLife Admin Portal

A modern, responsive admin dashboard for managing the NeuraLife mental health platform.

## 🌟 Features

### 🎨 Design & UI
- **Modern Interface**: Clean, professional design matching the main user portal
- **Dark Mode Toggle**: Switch between light and dark themes with persistent storage
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Smooth Animations**: Fade-in effects, hover transitions, and loading states
- **Color-coded Stats**: Visual indicators for different data types

### 📊 Dashboard Overview
- **Real-time Statistics**:
  - Total registered users
  - Premium members count
  - Active therapists
  - Total therapy sessions
- **Visual Cards**: Beautiful gradient cards with icons and stats
- **Auto-refresh**: Dashboard updates automatically

### 👥 User Management
- View all registered users
- Search users by username or email
- See user details:
  - Username and email
  - Premium status (Free/Premium)
  - NeuraCoins balance
  - Registration date
- **Quick Actions**:
  - Grant premium status
  - Revoke premium status
- Profile avatars with user initials

### 🩺 Therapist Management
- View all registered therapists
- Therapist information:
  - Name and email
  - Specialization
  - Avatar/emoji
  - Total sessions conducted
- Track therapist activity

### 📅 Session Management
- View all therapy session bookings
- Session details:
  - User and therapist names
  - Session type (In Person, Video Call, Chat)
  - Date and time
  - Status (pending, accepted, rejected, completed)
- Color-coded status indicators:
  - 🟡 Yellow: Pending
  - 🟢 Green: Accepted
  - 🔴 Red: Rejected
  - 🔵 Blue: Completed

### 📊 Quiz Results Analytics
- View all assessment completions
- Assessment data:
  - User who took the quiz
  - Assessment type (PHQ-9, GAD-7, PSS-10)
  - Score and result
  - Completion date
- Track mental health trends

### 🔐 Security
- Secure admin login
- Hardcoded credentials (admin1 / 123456)
- Session persistence
- Logout functionality

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+ installed
- NeuraLife backend running on `http://localhost:8000`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation & Setup

1. **Navigate to admin portal directory**:
   ```bash
   cd admin-portal
   ```

2. **Start the admin server** (Windows):
   ```bash
   start_admin.bat
   ```

   Or manually:
   ```bash
   python server.py
   ```

3. **Open in browser**:
   ```
   http://localhost:9000
   ```

4. **Login**:
   - Username: `admin1`
   - Password: `123456`

---

## 🎯 Usage Guide

### Login
1. Open `http://localhost:9000` in your browser
2. Enter credentials:
   - Username: **admin1**
   - Password: **123456**
3. Click "Sign In"

### Dashboard Navigation
- **Stats Cards**: View key metrics at the top
- **Tabs**: Click tabs to switch between sections:
  - 👥 Users
  - 🩺 Therapists
  - 📅 Sessions
  - 📊 Quiz Results

### User Management
1. Click "Users" tab
2. Use search bar to filter users
3. View user details in the table
4. Click "Grant Premium" or "Revoke Premium" to change status

### Dark Mode
- Click the 🌙 moon icon (light mode) or ☀️ sun icon (dark mode)
- Theme preference is saved automatically
- Applies to entire admin interface

### Logout
- Click "Logout" button in top-right corner
- Returns to login screen
- Clears admin session

---

## 🎨 Theme & Design

### Color Palette

#### Light Mode
- **Background**: Gradient blue/purple/pink (`#dbeafe → #e9d5ff → #fce7f3`)
- **Cards**: White (`#ffffff`)
- **Text**: Gray shades (`#1f2937`, `#6b7280`)
- **Accent**: Purple/Indigo gradient (`#667eea → #764ba2`)

#### Dark Mode
- **Background**: Gradient dark blue/purple (`#1e293b → #312e81 → #4c1d95`)
- **Cards**: Dark gray (`#1f2937`)
- **Text**: Light gray/white (`#f3f4f6`, `#ffffff`)
- **Accent**: Purple/Indigo gradient (same)

### Typography
- **Font**: Inter (Google Fonts)
- **Headings**: Bold, 24-32px
- **Body**: Regular, 14-16px
- **Labels**: Semibold, 12-14px

### Components
- **Buttons**: Rounded, gradient backgrounds, hover effects
- **Cards**: Rounded corners, shadows, hover animations
- **Tables**: Alternating row hover, responsive columns
- **Badges**: Rounded pills with color coding

---

## 🔌 API Endpoints

The admin portal connects to these backend endpoints:

### Statistics
- `GET /api/admin/users` - Get all users
- `GET /api/admin/therapists` - Get all therapists
- `GET /api/admin/sessions` - Get all sessions
- `GET /api/admin/quiz-results` - Get all quiz results
- `GET /api/admin/stats` - Get overall statistics

### Actions
- `PUT /api/admin/users/{username}/premium` - Toggle premium status

---

## 📱 Responsive Design

### Desktop (1024px+)
- 4-column stat cards
- Full-width tables
- Expanded navigation

### Tablet (768px - 1023px)
- 2-column stat cards
- Scrollable tables
- Compact navigation

### Mobile (< 768px)
- Single-column layout
- Stacked stat cards
- Mobile-optimized tables
- Hamburger menu (future)

---

## 🛠️ Technical Stack

### Frontend
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first styling via CDN
- **Vanilla JavaScript**: No frameworks, pure JS
- **CSS Grid & Flexbox**: Responsive layouts

### Backend Integration
- **Fetch API**: Async data loading
- **REST API**: JSON communication
- **CORS**: Cross-origin resource sharing

### Server
- **Python HTTP Server**: Built-in `http.server` module
- **Port**: 9000
- **Static files**: HTML, JS, CSS

---

## 🎭 Features Showcase

### Stats Cards
```
┌─────────────────────┐  ┌─────────────────────┐
│  👥                 │  │  ⭐                 │
│  Users              │  │  Premium            │
│                     │  │                     │
│  125                │  │  45                 │
│  Total Registered   │  │  Premium Members    │
└─────────────────────┘  └─────────────────────┘
```

### User Table
```
Username    Email           Premium    Coins    Actions
---------------------------------------------------------
test1       test1@...      ⭐ Premium   500    [Revoke]
newuser     new@...        Free          0     [Grant]
liban       liban@...      Free        1200    [Grant]
```

### Session Status Colors
- 🟡 **Pending**: Yellow badge
- 🟢 **Accepted**: Green badge
- 🔴 **Rejected**: Red badge
- 🔵 **Completed**: Blue badge

---

## 🚨 Troubleshooting

### Admin portal won't start
**Issue**: Server won't start on port 9000
**Solution**: 
```bash
# Check if port is in use
netstat -ano | findstr :9000

# Kill process if needed
taskkill /PID <PID> /F

# Or use different port in server.py
```

### Can't login
**Issue**: Credentials not working
**Solution**: 
- Verify username: `admin1` (all lowercase)
- Verify password: `123456`
- Clear browser cache and cookies
- Try incognito/private mode

### Data not loading
**Issue**: Tables are empty or show no data
**Solution**:
1. Verify backend is running on `http://localhost:8000`
2. Check browser console for errors (F12)
3. Verify CORS is enabled in backend
4. Test API endpoints directly:
   ```
   http://localhost:8000/api/admin/users
   ```

### Dark mode not persisting
**Issue**: Theme resets on page reload
**Solution**:
- Check browser allows localStorage
- Disable "Clear cookies on exit"
- Try different browser

---

## 🔒 Security Notes

### Current Implementation
- **Hardcoded credentials**: Username and password are in JavaScript
- **No encryption**: Login data sent in plain text
- **No session tokens**: Uses localStorage flag
- **No API authentication**: Admin endpoints are unprotected

### Production Recommendations
⚠️ **DO NOT use this in production without:**
1. **Real authentication**: JWT tokens, OAuth, or similar
2. **Encrypted connections**: HTTPS/SSL certificates
3. **API security**: Admin API key or token validation
4. **Rate limiting**: Prevent brute force attacks
5. **Audit logging**: Track admin actions
6. **Role-based access**: Different admin permission levels

---

## 📂 File Structure

```
admin-portal/
├── index.html          # Main HTML file
├── app.js             # JavaScript logic
├── server.py          # Python HTTP server
├── start_admin.bat    # Windows startup script
└── README.md          # This file
```

---

## 🎯 Future Enhancements

### Planned Features
- [ ] Export data to CSV/Excel
- [ ] Advanced filtering and sorting
- [ ] Data visualization charts (graphs, pie charts)
- [ ] Bulk operations (batch premium grants)
- [ ] Email notification system
- [ ] User activity timeline
- [ ] Therapist performance metrics
- [ ] Revenue analytics
- [ ] System health monitoring
- [ ] Real-time updates (WebSocket)

### UI Improvements
- [ ] Mobile hamburger menu
- [ ] Pagination for large tables
- [ ] Column sorting
- [ ] Advanced search filters
- [ ] Data export buttons
- [ ] Confirmation modals
- [ ] Toast notifications
- [ ] Loading skeletons

---

## 📞 Support

For issues or questions:
1. Check browser console (F12) for errors
2. Verify backend is running
3. Review this README
4. Check CORS settings in backend

---

## 📄 License

Part of the NeuraLife platform. All rights reserved.

---

## 🎉 Credits

**Design**: Modern admin dashboard inspired by contemporary SaaS platforms
**Theme**: Matches NeuraLife user portal branding
**Icons**: Emoji-based for universal compatibility

---

**Happy Managing! 🚀**
>>>>>>> 8f42418579ec6d512ce83ecf248d8ad6a4c96c7f
