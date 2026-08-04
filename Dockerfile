FROM ubuntu:latest
LABEL authors="anshul"

ENTRYPOINT ["top", "-b"]