# Running Greasy Fork locally

This document summarizes the steps required to run Greasy Fork locally, adapted from the official Greasy Fork wiki: https://github.com/greasyfork-org/greasyfork/wiki/Running-Greasy-Fork-locally

Use this as a quick-start reference. For any repository-specific details, consult the Greasy Fork repo's README and wiki.

## Prerequisites

- Ruby (use the version specified in the repository, check `.ruby-version` or the Gemfile)
- Bundler (`gem install bundler`)
- Node.js and Yarn (for JS assets)
- PostgreSQL (or the DB configured by the repo)
- ImageMagick (for image processing tasks)
- Build tools for any native gems (e.g., gcc, make, libpq-dev on Debian/Ubuntu)

## Quick setup

1. Clone the repository

   git clone https://github.com/greasyfork-org/greasyfork.git
   cd greasyfork

2. Install Ruby gems

   bundle install

3. Install JavaScript dependencies

   yarn install

4. Configure database

   - Edit `config/database.yml` if necessary to match your local PostgreSQL user/password/host/port
   - Create the database, load schema, and seed (if provided):

     bundle exec rails db:setup

   - Alternatively:

     bundle exec rails db:create
     bundle exec rails db:migrate
     bundle exec rails db:seed

5. Set environment variables / credentials

   - Provide any required ENV vars (secrets, API keys, etc.). Many projects use `.env` or Rails credentials.
   - Example (replace values as needed):

     export RAILS_ENV=development
     export SECRET_KEY_BASE=your_secret_key
     export DATABASE_URL=postgres://user:pass@localhost/greasyfork_dev

6. Start background workers (if used)

   If the project uses Sidekiq or another background processor, start it separately:

   bundle exec sidekiq

7. Run the Rails server

   bundle exec rails server

   By default the app will be available at http://localhost:3000

## Optional: Docker

If the project provides Docker support (check for `Dockerfile` / `docker-compose.yml`), you can run with Docker Compose:

   docker-compose up --build

This can simplify installing dependencies like PostgreSQL and Redis locally.

## Notes & troubleshooting

- If `bundle install` or native gems fail, ensure system dependencies for libraries (libpq-dev, imagemagick, ffmpeg, etc.) are installed.
- Check the repository's README or wiki for project-specific ENV vars, secrets, or setup steps.
- Use `rails log:tail` or `tail -f log/development.log` to stream logs while reproducing issues.

---

Reference: https://github.com/greasyfork-org/greasyfork/wiki/Running-Greasy-Fork-locally
