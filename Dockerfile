FROM python:3.12-bookworm
WORKDIR /app
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip -r /requirements.txt && \
    playwright install --with-deps

COPY . .

ENV BASE_URL=https://www.kiwi.com

EXPOSE 9222

CMD ["pytest"]