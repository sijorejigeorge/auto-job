# Use official Python image
FROM python:3.11-slim

# Install Playwright dependencies using the official script
RUN pip install --no-cache-dir playwright && python -m playwright install --with-deps

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Install Playwright browsers
RUN python -m playwright install

# Copy project files
COPY . .

# Default command (update main.py as needed)
CMD ["python", "main.py"]
