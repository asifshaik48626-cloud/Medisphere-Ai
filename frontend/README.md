# MediSphere AI - Frontend Portal

This directory contains the React-TypeScript single-page web app built with Vite and styled using Tailwind CSS.

## 🛠 Prerequisites

- Node.js 18+
- npm (Node Package Manager)

## 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Configure Tailwind Style Briefs**:
   Custom color palettes (`#0F5F5C` clinical teal, mint, warm amber, red alerts) and Google Fonts (Inter/Outfit) are automatically managed through `tailwind.config.js` and loaded dynamically.

3. **Start Vite Development Server**:
   ```bash
   npm run dev
   ```
   Open `http://localhost:3000` in your web browser. All requests to `/api` are automatically proxied to port 8000 (FastAPI).

## 🔑 Test Credentials

Use these seeded logins during development:
- **Patient Dashboard**: `patient@medisphere.com` / `password123`
- **Clinician Dashboard**: `doctor@medisphere.com` / `password123`
- **Admin Dashboard**: `admin@medisphere.com` / `password123` *(Select bypass or seed credentials)*
