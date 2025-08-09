# RSP Education Agent V2 - Docker Management
# Simple commands to manage the entire Docker setup

# Default goal
.DEFAULT_GOAL := help

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Help command
.PHONY: help
help: ## Show this help message
	@echo "$(GREEN)RSP Education Agent V2 - Docker Commands$(NC)"
	@echo "================================================"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Setup commands
.PHONY: setup
setup: ## Initial setup - copy environment file
	@echo "$(GREEN)Setting up RSP Education Agent V2...$(NC)"
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(YELLOW)Created .env file from template$(NC)"; \
		echo "$(RED)⚠️  Please edit .env and add your API keys!$(NC)"; \
	else \
		echo "$(YELLOW).env file already exists$(NC)"; \
	fi

# Build commands
.PHONY: build
build: ## Build all Docker images
	@echo "$(GREEN)Building all Docker images...$(NC)"
	docker-compose build --no-cache

.PHONY: build-backend
build-backend: ## Build only backend Docker image
	@echo "$(GREEN)Building backend Docker image...$(NC)"
	docker-compose build --no-cache backend

.PHONY: build-frontend
build-frontend: ## Build only frontend Docker image
	@echo "$(GREEN)Building frontend Docker image...$(NC)"
	docker-compose build --no-cache frontend

# Run commands
.PHONY: up
up: ## Start all services
	@echo "$(GREEN)Starting RSP Education Agent V2...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Services started!$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:3000$(NC)"
	@echo "$(YELLOW)Backend API: http://localhost:8000$(NC)"
	@echo "$(YELLOW)API Docs: http://localhost:8000/docs$(NC)"

.PHONY: up-dev
up-dev: ## Start all services with logs visible
	@echo "$(GREEN)Starting RSP Education Agent V2 in development mode...$(NC)"
	docker-compose up

.PHONY: down
down: ## Stop all services
	@echo "$(GREEN)Stopping all services...$(NC)"
	docker-compose down

.PHONY: restart
restart: down up ## Restart all services

# Database commands
.PHONY: db-reset
db-reset: ## Reset database (WARNING: This will delete all data!)
	@echo "$(RED)⚠️  This will delete all database data!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose down -v
	docker volume rm rsp_education_app_v2_postgres_data || true
	docker volume rm rsp_education_app_v2_redis_data || true
	docker-compose up -d database redis
	@echo "$(GREEN)Database reset complete$(NC)"

.PHONY: db-backup
db-backup: ## Backup database
	@echo "$(GREEN)Creating database backup...$(NC)"
	docker-compose exec database pg_dump -U rsp_user rsp_education > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)Database backup created$(NC)"

# Logs and monitoring
.PHONY: logs
logs: ## View logs from all services
	docker-compose logs -f

.PHONY: logs-backend
logs-backend: ## View backend logs
	docker-compose logs -f backend

.PHONY: logs-frontend
logs-frontend: ## View frontend logs
	docker-compose logs -f frontend

.PHONY: logs-db
logs-db: ## View database logs
	docker-compose logs -f database

# Status and health
.PHONY: status
status: ## Check status of all services
	@echo "$(GREEN)Service Status:$(NC)"
	docker-compose ps

.PHONY: health
health: ## Check health of all services
	@echo "$(GREEN)Health Check:$(NC)"
	@echo "Backend: $$(curl -s -o /dev/null -w "%%{http_code}" http://localhost:8000/health || echo "DOWN")"
	@echo "Frontend: $$(curl -s -o /dev/null -w "%%{http_code}" http://localhost:3000/health || echo "DOWN")"
	@echo "Database: $$(docker-compose exec -T database pg_isready -U rsp_user -d rsp_education > /dev/null 2>&1 && echo "UP" || echo "DOWN")"

# Testing
.PHONY: test
test: ## Run UAT tests
	@echo "$(GREEN)Running UAT tests...$(NC)"
	docker-compose exec backend python test_uat_readiness.py

.PHONY: test-backend
test-backend: ## Run backend unit tests
	@echo "$(GREEN)Running backend tests...$(NC)"
	docker-compose exec backend pytest tests/ -v

# Development commands
.PHONY: shell-backend
shell-backend: ## Access backend container shell
	docker-compose exec backend bash

.PHONY: shell-db
shell-db: ## Access database shell
	docker-compose exec database psql -U rsp_user -d rsp_education

.PHONY: shell-redis
shell-redis: ## Access Redis CLI
	docker-compose exec redis redis-cli

# Cleanup commands
.PHONY: clean
clean: ## Remove stopped containers and unused images
	@echo "$(GREEN)Cleaning up Docker resources...$(NC)"
	docker-compose down
	docker system prune -f
	docker volume prune -f

.PHONY: clean-all
clean-all: ## Remove everything (containers, images, volumes)
	@echo "$(RED)⚠️  This will remove all Docker resources!$(NC)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose down -v --remove-orphans
	docker system prune -a -f
	docker volume prune -f

# Production commands
.PHONY: prod-up
prod-up: ## Start in production mode with Nginx proxy
	@echo "$(GREEN)Starting in production mode...$(NC)"
	docker-compose --profile production up -d

.PHONY: prod-build
prod-build: ## Build for production
	@echo "$(GREEN)Building for production...$(NC)"
	docker-compose --profile production build --no-cache

# Quick commands
.PHONY: quick-start
quick-start: setup build up ## Complete setup and start (first time users)
	@echo "$(GREEN)🎉 RSP Education Agent V2 is now running!$(NC)"
	@echo "$(YELLOW)📱 Frontend: http://localhost:3000$(NC)"
	@echo "$(YELLOW)🔧 Backend: http://localhost:8000$(NC)"
	@echo "$(YELLOW)📚 API Docs: http://localhost:8000/docs$(NC)"
	@echo "$(RED)⚠️  Don't forget to add your API keys to .env file!$(NC)"

.PHONY: daily-start
daily-start: up ## Quick start for daily development
	@echo "$(GREEN)Ready for development! 🚀$(NC)"