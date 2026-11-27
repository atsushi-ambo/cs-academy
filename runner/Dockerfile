FROM python:3.13-slim@sha256:7249d5587b78209a006dc4a3b5340678f84ea729239193aa559962cd8c1fce50
WORKDIR /tmp
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip uninstall -y pip \
    && rm -rf /usr/local/lib/python3.13/ensurepip \
    && install -d -m 0755 /opt/academy
COPY --chmod=0444 sandbox.py /opt/academy/sandbox.py
USER 65532:65532
ENTRYPOINT ["python", "-I", "-B", "-u", "/opt/academy/sandbox.py"]
