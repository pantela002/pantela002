# Notes

A private notes app: one login (yours), notes stored in Supabase, hosted on Vercel at
`notes.pantelicu.space`. Plain HTML/CSS/JS, no build step.

**How it stays private:** you log in with Supabase Auth (email + password). The `notes`
table has Row Level Security, so the database only returns rows whose `user_id` is the
logged-in user, and returns nothing to anyone not logged in. Once your account exists you
turn off sign-ups, so nobody else can ever get a login.

## 1. Supabase

1. **Create the table.** Supabase dashboard → your project → **SQL Editor** → New query →
   paste all of [`supabase/schema.sql`](supabase/schema.sql) → **Run**.
2. **Create your account.** **Authentication → Users → Add user → Create new user**.
   Enter your email and a strong password and tick **Auto Confirm User**.
3. **Turn off sign-ups.** **Authentication → Sign In / Providers** (older dashboards:
   *Providers → Email*) → switch off **Allow new users to sign up** → Save.
   Keep the Email provider itself enabled, or you can't log in either.
4. **Copy your keys.** **Project Settings → API** (or the **Connect** button): copy the
   **Project URL** and the **anon** / **publishable** key into [`config.js`](config.js).
   Do *not* use the `service_role` / secret key; that one bypasses all security.

## 2. Vercel

1. Push this folder to its own GitHub repo (for example `pantela002/notes`).
2. Vercel → **Add New… → Project** → import that repo.
   Framework preset: **Other**. No build command, no output directory. **Deploy**.
3. Open the `*.vercel.app` link and log in to check it works.

## 3. Domain: notes.pantelicu.space

1. Vercel → the project → **Settings → Domains** → add `notes.pantelicu.space`.
   Vercel shows the DNS record it wants; use exactly that.
2. Namecheap → **Domain List → pantelicu.space → Manage → Advanced DNS → Add new record**:
   - Type: **CNAME Record**
   - Host: **notes**
   - Value: what Vercel showed (usually `cname.vercel-dns.com`)
   - TTL: Automatic
3. Wait for Vercel to show the domain as valid (minutes, sometimes up to an hour).
   HTTPS is set up automatically.
4. Supabase → **Authentication → URL Configuration**: set **Site URL** to
   `https://notes.pantelicu.space` and add it under **Redirect URLs**.

## Using it

- **+ New note**, type, then **Save** (or Ctrl/Cmd+S).
- Click a note to edit it, **Delete** to remove it, search box filters by title and text.
- Forgot your password? Supabase → **Authentication → Users** → your user → set a new one.

## Files

| File | What it is |
|---|---|
| `index.html` | Login screen and notes screen |
| `app.js` | Login, loading, saving, deleting notes (Supabase JS client) |
| `style.css` | Styles, light and dark, works on phone |
| `config.js` | Your Supabase URL and anon key |
| `supabase/schema.sql` | Table + Row Level Security, run once |
| `vercel.json` | Security headers, tells search engines not to index |
