FROM python:3.13.11-slim

# get uv from another docker image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# copy host uv specs from host machine
WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"
COPY pyproject.toml .python-version uv.lock ./

# installs deps from uv lock file
RUN uv sync --locked

# RUN pip install pandas pyarrow

COPY pipeline.py .

ENTRYPOINT [ "python", "pipeline.py"]