FROM python:3.9-slim

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Accept GitHub token as build argument
ARG GITHUB_TOKEN

# Clone the publish repository using the token
RUN git clone https://${GITHUB_TOKEN}@github.com/jpl-labcas/publish.git /app

WORKDIR /app

# (Optional) Install any dependencies if required by the publish repo
# RUN pip install -r requirements.txt

CMD ["bash"]