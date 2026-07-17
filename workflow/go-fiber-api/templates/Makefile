.PHONY: run build test vet clean lint dev

run:
	go run ./cmd/server/

build:
	go build -o bin/server ./cmd/server/

test:
	go test ./...

vet:
	go vet ./...

clean:
	rm -rf bin/

lint: vet
	@echo "lint done"

dev:
	@echo "Starting with air..." && air
