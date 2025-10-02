# Schedule_Sifter

A tiny web app to save personal schedules and quickly find common free time with friends/teammates.

What it does

Sign in (session-based auth) and use the app

Create rooms and invite others (QR link)

Save your schedule (timezone + busy intervals)

View your schedules (and room members’ schedules)

Compare room members to find shared availability

Tech

Frontend: static HTML/CSS/JS in /client (served by Express)

Backend: Node.js + Express in /server

DB: MongoDB (Atlas compatible) via Mongoose

Validation: Zod

Auth: session-based (requireAuth) with Google OAuth; optional local auth



App serves on http://localhost:4000

Setup with:
cd server
npm install

Run the app from inside server, with:
npm run dev


