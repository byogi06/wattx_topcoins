#Dockerfile, build image , Container
FROM python:3.8
WORKDIR /pricing_app
ADD . /pricing_app
COPY ./requirement.txt .
RUN pip install -r requirement.txt
COPY . .
EXPOSE 5002
ENTRYPOINT ["python"]
CMD ["pricing_service.py"]