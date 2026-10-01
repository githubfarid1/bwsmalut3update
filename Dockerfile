FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# create settings.py from sample if not exists
RUN if [ ! -f core/settings.py ]; then cp core/settings.py.sample core/settings.py; fi

# collect static files
RUN python manage.py collectstatic --noinput 2>/dev/null || true

# gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "core.wsgi"]
