## Run Dockerfile

Create a new image with the command below, where you choose the name of the image.

```console
docker build -t <IMAGE_NAME> .
```

To run the image:

```console
docker run -d -p 5000:5000 <IMAGE_NAME>
```
