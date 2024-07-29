# Use the official Alpine image
FROM python:3.11-alpine


# Install system dependencies
RUN apk update && apk add --no-cache bash \
    chromium \
    chromium-chromedriver \
    xvfb-run

COPY . /app
WORKDIR /app/
RUN pip install --no-cache-dir /app/
RUN rm -rf /app/

RUN addgroup -S service && adduser -S service -G service
USER service
EXPOSE 8080
CMD ["python3", "-m", "poept.server"]