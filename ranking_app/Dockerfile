#Dockerfile, build image , Container
FROM python:3.8
WORKDIR /ranking_app
ADD . /ranking_app
COPY ./requirement.txt .
RUN pip install -r requirement.txt
COPY . .
EXPOSE 5001
ENTRYPOINT ["python"]
CMD ["ranking_service.py"]
