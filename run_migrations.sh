#!/bin/bash
# Script to run migrations in the correct order
# Ensures Django's built-in migrations run first, then core.User model

set -e

echo "Running migrations in correct order..."

# First, ensure contenttypes and auth migrations are applied
# These are required for the custom User model
echo "Step 1: Running contenttypes migrations..."
python3 manage.py migrate contenttypes --noinput

echo "Step 2: Running auth migrations..."
python3 manage.py migrate auth --noinput

# Now run core migrations to create the User model
echo "Step 3: Running core migrations..."
python3 manage.py migrate core --noinput

# Finally, run all remaining migrations (admin, sessions, etc.)
echo "Step 4: Running all remaining migrations..."
python3 manage.py migrate --noinput

echo "Migrations complete!"

# Show migration status for debugging
echo "Current migration status:"
python3 manage.py showmigrations
