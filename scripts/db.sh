#!/bin/bash

# Database management script for autograb project

set -e

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed."
    echo "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Determine docker-compose command
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "Error: Neither docker-compose nor docker compose is available."
    echo "Please install Docker Compose or update Docker Desktop."
    exit 1
fi

case "$1" in
    "start")
        echo "Starting PostgreSQL database..."
        $DOCKER_COMPOSE up -d
        echo "Database started! Connection details:"
        echo "  Host: localhost"
        echo "  Port: 5432"
        echo "  Database: autograb"
        echo "  Username: autograb_user"
        echo "  Password: autograb_password"
        ;;
    "stop")
        echo "Stopping PostgreSQL database..."
        $DOCKER_COMPOSE down
        ;;
    "restart")
        echo "Restarting PostgreSQL database..."
        $DOCKER_COMPOSE restart
        ;;
    "reset")
        echo "Resetting PostgreSQL database (this will delete all data)..."
        $DOCKER_COMPOSE down -v
        $DOCKER_COMPOSE up -d
        echo "Database reset complete!"
        ;;
    "logs")
        $DOCKER_COMPOSE logs -f postgres
        ;;
    "connect")
        echo "Connecting to PostgreSQL database..."
        $DOCKER_COMPOSE exec postgres psql -U autograb_user -d autograb
        ;;
    "seed")
        echo "Seeding database with sample data..."
        $DOCKER_COMPOSE exec postgres psql -U autograb_user -d autograb -f /docker-entrypoint-initdb.d/01-init.sql
        echo "Database seeded successfully!"
        ;;
    "seed-fresh")
        echo "Resetting and seeding database with fresh data..."
        $DOCKER_COMPOSE down -v
        $DOCKER_COMPOSE up -d
        echo "Waiting for database to be ready..."
        sleep 5
        echo "Database reset and seeded successfully!"
        ;;
    "status")
        echo "Database status:"
        $DOCKER_COMPOSE ps
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|reset|logs|connect|seed|seed-fresh|status}"
        echo ""
        echo "Commands:"
        echo "  start      - Start the database"
        echo "  stop       - Stop the database"
        echo "  restart    - Restart the database"
        echo "  reset      - Reset the database (delete all data)"
        echo "  logs       - Show database logs"
        echo "  connect    - Connect to database with psql"
        echo "  seed       - Seed database with sample data"
        echo "  seed-fresh - Reset and seed database with fresh data"
        echo "  status     - Show database status"
        exit 1
        ;;
esac 