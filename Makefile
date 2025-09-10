# Makefile pro automatizaci DaPTools integrace

.PHONY: update-daptools build-deps dev clean web

# Aktualizuje DaPTools a rebuild kontejner
update-daptools:
	@echo "Building DaPTools..."
	cd ../DaPTools && poetry build
	@echo "Copying wheel to strojarina..."
	cp ../DaPTools/dist/*.whl wheels/
	@echo "Rebuilding container..."
	docker build -t strojarina:latest . --no-cache

# Pouze build DaPTools wheel
build-deps:
	cd ../DaPTools && poetry build
	cp ../DaPTools/dist/*.whl wheels/

# Development s hot reload
dev: update-daptools
	docker run -it --rm -v $(PWD):/app strojarina:latest bash

# Web GUI mode
web: update-daptools
	docker run -it --rm \
		-v $(PWD):/app \
		-p 5000:5000 \
		strojarina:latest
	@echo "Web GUI dostupné na: http://localhost:5000"

# Vyčistí staré wheels
clean:
	rm -f wheels/*.whl
	docker image prune -f