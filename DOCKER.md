# aws-lambda-s3-copy-zips

Using GitHub Actions and Python to copy AWS Lambda zip files across S3 buckets

Project Status: **Stable**

# Purpose

This Python script copies S3 objects from mutliple S3 source buckets to multiple S3 destination buckets  

# Usage

1. Run Docker container using
`docker run --network host -itd aws-lambda-s3-copy-zips:latest`
2. To configure the source and destination buckets and which objects get copied, copy the `config.json.example` file into `config.json`. For more information on the configuration variables available to you, refer the Configuration section of the documentation.
3. (Optional) Alternatively you could use environment variables to configure the script but it is limited to 1 source bucket and 1 destination bucket. TODO: Multiple destination buckets.

## Configuration

| `config.json` file | Config as Environment variable(s) | Description |
|---------------|-----------------------------|-------------|
| `srcBucket` | `SRC_BUCKET` | In JSON, this is an list of source regions and buckets in those regions. When using environment variable `SRC_BUCKET`, this is the name of the source S3 bucket |
| :x: | `SRC_REGION` | Only available when the script falls back to  environment variables in the absence of a `config.json` file. This is the region of the source S3 bucket |
| :x: | `SRC_KEY_PREFIX` | Only available when the script falls back to  environment variables in the absence of a `config.json` file. This is the prefix of the S3 object from the root of the S3 bucket |
| :x: | `SRC_KEY` | Only available when the script falls back to  environment variables in the absence of a `config.json` file. This is the name of the S3 object that needs to be copied |
| `dstBucket` | `DST_BUCKET` | In JSON, this is an list of destination regions and buckets in those regions. When using environment variable `DST_BUCKET`, this is the name of the destination S3 bucket |
| :x: | `DST_REGION` | Only available when the script falls back to  environment variables in the absence of a `config.json` file. This is the region of the destination S3 bucket |

# Compatibility

| Environment | Status |
|-------|------|
| `GitHub Actions` | :white_check_mark: |
| `Docker` (local) | :white_check_mark: |
| `CLI` | :construction: Needs Docker/Python |

## GitHub Actions

```
    - name: Copy AWS Lambda zip file from 1:1 S3 bucket
      uses: GeorgeDavis-Ibexlabs/aws-lambda-s3-copy-zips@v0.0.1
```
Refer to [Copy AWS Lambda zip files across S3 buckets using GitHub Actions](https://github.com/marketplace/actions/aws-lambda-s3-copy-zips)

# Issues?

For any issues or errors with this script, please raise an [issue here](https://github.com/GeorgeDavis-Ibexlabs/aws-lambda-s3-copy-zips/issues)

# Contribute

If you encounter a bug or think of a useful feature, or find something confusing in the docs, please create a new issue.

I ♥️ pull requests. If you'd like to fix a bug or contribute to a feature or simply correct a typo, please feel free to do so.

If you're thinking of adding a new feature, consider opening an issue first to discuss it to ensure it aligns with the direction of the project and potentially save yourself some time.

## Development

```sh
docker login
```

```sh
docker build --no-cache --progress=plain . -f Dockerfile -t aws-lambda-s3-copy-zips:latest 2>&1 | tee build.log
```

```sh
docker run --network host -itd \
-e LOGLEVEL='DEBUG' \
aws-lambda-s3-copy-zips:latest
```

> Use log levels available within the Python `logging` library as values for `LOGLEVEL`