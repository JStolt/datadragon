# DataDragon

## Docker

### Build Container Image

```bash
docker build -t datadragon:0.1 .
```

### Run Container

```bash
docker run --rm -it \
    -p 5432:5432 \
    -v $(pwd)/example-data/csv:/data \
    -e POSTGRES_DB=datadragon \
    -e POSTGRES_USER=datadragon \
    -e POSTGRES_PASSWORD=datadragon \
    datadragon:0.1
```