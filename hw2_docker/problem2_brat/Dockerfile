FROM scratch
RUN mkdir -p /src/app
COPY ./brat-v1.3_Crunchy_Frog/ /src/app
WORKDIR /src/app
RUN  install.sh -u
CMD ["python", "/src/app/standalone.py"]
