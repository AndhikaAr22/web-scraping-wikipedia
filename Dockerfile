FROM python:3.11-bookworm

WORKDIR /root/web_scraping

COPY ./requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

CMD ["python", "main.py"]
